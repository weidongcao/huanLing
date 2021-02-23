#!/bin/bash
# @author CaoWeidong
# @time 2021-02-23 14:46:34
# 命令行传参
# -d|--days:导入之前多少小时的数据(默认最近7天)
# -p|--pattern:过滤条件(正则表达式)(默认wedo|weidong)
# -n|--thread_num:开多少个线程(默认开3个线程)
# -D|--data_path:数据目录(默认/home/wedo/20201222)
# -c|--column_count:一条数据的字段个数(默认为9,不是9的话都会被过滤掉)
# --help:使用帮助
#
# 例子：
# sh export_data.sh -d -100 -p "qq.com|taobao.com|tmall.com" -n 10 -D /home/wedo/20201222 -c 9
# -d -100: 意为导入最近100天的数据, 
# -p "qq.com|taobao.com|tmall.com": 过滤条件的匹配模式为 qq.com或者taobao.com或者tmall.com，
# -n 10: 开10个线程导数据，
# -D /home/wedo/20201222: 导/home/wedo/20201222目录下的数据
# -c 9: 1行数据有9个字段
#
# 以上参数均可选，没有的话有默认值
# 导出的数据会存储在data_{pid}目录下，{pid}为一串数字，
# 如果多次导入的话看下任务主进程的PID是多少，就知道对应的数据在哪个目录下
# 主进程PID在日志文件里看, 日志文件为脚本同名的.log文件
############################ 打印变量值,调试时打开 ############################
#set -e
#set -x

function get_timestamp(){
    echo $(($(date +%s%N) / 1000000))
}

# 打印日志
function logger(){
    echo "$(date "+%Y-%m-%d %H:%M:%S") [INFO] ${1}"
    echo "$(date "+%Y-%m-%d %H:%M:%S") [INFO] ${1}" >> "${0/sh/log}"
}

################################## 初始化变量 ##################################
# 当前路径
cur_dir="$(cd "$( dirname "$0"  )" && pwd)"
# 脚本主线程PID作为数据生成目录
main_pid="$$"
# 数据目录(随机生成)
data_path="/home/wedo/20201222"
output_path="${cur_dir}/data_${main_pid}"
#需要过滤的字符串正则表达式
pattern="wedo|weidong"
days=-7
#字段个数
column_count=9
# 线程数
thread_num=3


ARGS=$(getopt -a -o d:p:n:c:D: --long days:,pattern:,thread_num:,data_path:,column_count:,help -- "$@")

# 重排选项
if [ $? != 0 ];then
    echo "Terminating..."
    exit 1
fi


eval set -- "${ARGS}"


# 解析命令行参数
while :
do
    case "$1" in
        -d|--days)
            days=${2}
            shift
            ;;
        -p|--pattern)
            pattern=${2}
            shift
            ;;
        -n|--thread_num)
            thread_num=${2}
            shift
            ;;
        -c|--column_count)
            column_count=${2}
            shift
            ;;
        -D|--data_path)
            data_path=${2}
            shift
            ;;
        --help)
            usage
            ;;
        --)
            shift
            break
            ;;
        *)
            logger "thread-main $1"
            logger "thread-main Internal error!"
            exit 1
            ;;
    esac
        shift
done
logger "thread-main 主线程PID: $$"
logger "thread-main 导出最近 $((0 - days)) 天的数据"
logger "thread-main 过滤条件为: ${pattern}"
logger "thread-main 开启线程数: ${thread_num}"
logger "thread-main 源数据目录: ${data_path}"
logger "thread-main 一条数据的字段个数: ${column_count}"
logger "thread-main 输出目录: ${output_path}"

# 判断数据目录是否存在
if [[ ! -d "{output_path}" ]];then
    logger "thread-main output path does not exist, I will create it: ${output_path}"
    mkdir -p "${output_path}"
fi


################################## 初始化多线程 ##################################
temp_fifofile="$$.fifo"
mkfifo $temp_fifofile

# 将fd6指向fifo类型
# 使文件描述符为非阻塞式
exec 6<>$temp_fifofile
rm $temp_fifofile

#根据线程总数量设置令牌个数
for ((i = 0;i < thread_num;i++));do
    echo
done >&6
logger "thread-main multiple thread init finish, thread number: ${thread_num}"


# 1. 通过find命令获取数据目录下指定时间段的数据文件
#       1. 读取1个线程令牌以创建1个子线程,如果没有令牌等待
#       2. 执行导入命令
# 2. 导入所有find出来的文件后,等待所有子线程执行完毕
#
# 3. 关闭线程流及令牌
# 4. 删除数据目录
# 获取数据目录下最近多少分钟修改过的数据文件
file_count=$(find "${data_path}" -name "*.gz" -mtime "${days}" | wc -l)
export_count=0
for file in $(find "${data_path}" -name "*.gz" -mtime "${days}" | sort) ; do

	# 获取1个令牌
	read -u6

	# 创建子线程执行导入
	{
		# 线程号
		thread_id="thread-$(printf '%04d' $((RANDOM % 10000)))"

		#output_file=$(stat ${file} | grep -E "Modify|最近更改" | awk '{printf "%s_%s",$2,$3}')
		#output_file="${output_path}/${output_file:0:13}.out"
		output_file="${file##*/}"
		output_file="${output_path}/${output_file}.out"

		# 导入数据命令模板
		import_cmd="zcat ${file} | grep -E \"${pattern}\" | awk -F \"|\" '{if(NF == ${column_count}) print }' >> ${output_file}"

		# 该线程导入开始时间
		start_time=$(get_timestamp)

		# 执行导入命令
		eval "${import_cmd}"

		# 判断是否导入成功，不成功仅提示错误
		if [ $? -eq 0 ]; then
			# 导入成功后增加换行,不然前后两个文件轮换的时候可能会出现2行拼接成1行
			if [  -s ${output_file} ]; then
				echo "" >> ${output_file}
			fi
			# 记录导入命令执行时间
			import_time=$(get_timestamp)
			if [ $(( export_count % 10 )) -eq 0 ]; then
				logger "${thread_id} import success, execution time:  $(printf '%5d' $((import_time - start_time))) millisecond, data file: ${file##*/}"
				logger "${thread_id} export file count: ${export_count}/${file_count}"
			fi

		else
			# 导入失败，提示错误
			logger "${thread_id} DNS日志导入ClickHouse失败,命令:${import_cmd}"
			sleep 10
			#exit -1
		fi

		# 返还令牌
		echo "" >&6
	} &
	((export_count++))
done
logger "${thread_id} export file count: ${export_count}/${file_count}"
logger "thread-main finish import find files ..."

# 等待所有子线程结束
wait

# 删除线程流及令牌
exec 6>&-

logger "thread-main --> over"

