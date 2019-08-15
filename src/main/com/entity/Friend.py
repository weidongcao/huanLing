
class Friend:
	def __init__(self):
		self.name = None
		self.age = None
		self.birthday = None
		self.city = None
		self.hometown = None

	def __init__(self, name, age, birthday, city, hometown):
		self.name = name
		self.age = age
		self.birthday = birthday
		self.city = city
		self.hometown = hometown

	def toString(self):
		print("name = {}, age = {}".format(self.name, self.age))

	def toJSON(self):
		obj = {
			"name": self.name,
			"age": self.age,
			"birthday": self.birthday,
			"city": self.city,
			"hometown": self.hometown
		}
		return obj

