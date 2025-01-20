class OutputProfessor(object):
    def __init__(self, name, department, school, courses=[]):
        self.firstName = name.split(" ")[0]
        self.lastName = name.split(" ")[1]
        self.department = department
        self.school = school
        self.courses = courses

    def __str__(self):
        return "Name: " + self.name

    def toCsvString(self):
        return self.name + "," + self.department