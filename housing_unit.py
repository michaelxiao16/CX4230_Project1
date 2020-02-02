class HousingUnit:
    """ A class to represent a housing unit in the simulation

    Price per year (determined by factors below)
    Rent or own status
    Crime rating
    Education rating
    Distance to business center
    """

    def get_price(self):
        return self.price

    def get_status(self):
        return self.status

    def get_crime(self):
        return self.crime

    def get_education(self):
        return self.education

    def get_distance(self):
        return self.distance

    def __init__(self, price, status, crime, education, distance):
        self.price = price
        self.status = status
        self.crime = crime
        self.education = education
        self.distance = distance
