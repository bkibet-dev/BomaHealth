class Person:
    all_people = []
    def __init__(self, name, person_id, role):
        self.name = name
        self.person_id = person_id
        self.role = role
        Person.all_people.append(self)
    @classmethod
    def get_all_people(cls):
        return cls.all_people
class CHP(Person):
    def __init__(self, name, person_id):
        super().__init__(name, person_id, role="chp")
        self.households = []
    def add_household(self, household):
        self.households.append(household)