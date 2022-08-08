import json


class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def info(self):
        return {"name": self.name, "age": self.age, "gender": self.gender}

    def to_json(self):
        return {Person.__name__: self.info()}


class Student(Person):
    def __init__(self, name, age, gender, clz):
        Person.__init__(self, name, age, gender)
        self.clz = clz

    def info(self):
        obj = super(Student, self).info()
        obj["clz"] = self.clz
        return obj

    def to_json(self):
        return {Student.__name__: self.info()}

    def learn(self):
        return "I'm learn in {}".format(self.clz)


class Worker(Person):
    def __init__(self, name, age, gender, profession):
        super(Worker, self).__init__(name, age, gender)
        self.profession = profession

    def info(self):
        obj = super(Worker, self).info()
        obj["profession"] = self.profession
        return obj

    def to_json(self):
        return {Worker.__name__: self.info()}

    def work(self):
        return "I'm working in {}".format(self.profession)


def task():
    s = Student("WangMingyang", 18, False, "senior")
    w = Worker("CaoWeidong", 29, True, "bigdata")
    js = json.dumps(s, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)


    print(js)

if __name__ == '__main__':
    task()
