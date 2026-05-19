
class person :
    def __init__(self,name,year,branch):
        self.name = name
        self.year = year,
        self.branch = branch


class male(person):
    def __init__(self, name, year, branch):
        super().__init__(name, year, branch)
        self.gender = "male"

if __name__ == "__main__":
    pass