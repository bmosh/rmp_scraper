class OutputProfessor(object):
    def __init__(self, name, department, school, courses=[]):
        self.firstName = name.split(" ")[0]
        self.lastName = name.split(" ")[1]
        self.school = school
        self.department = department
        self.courses = courses

    def __str__(self):
        return "Name: " + self.name + "\nDepartment: " + self.department + "\nQuality: " + str(self.quality) + "\nDifficulty: " + str(self.difficulty) + "\nWould Take Again: " + str(self.would_take_again) + "\nAverage GPA: " + str(self.avg_gpa) + "\nNumber of Ratings: " + str(self.num_of_ratings)

    def toCsvString(self):
        return self.name + "," + self.department + "," + str(self.quality) + "," + str(self.difficulty) + "," + str(self.would_take_again) + "," + str(self.avg_gpa) + "," + str(self.num_of_ratings)