class HousingUnit:
    """ A class to represent a housing unit in the simulation

    Price per year (determined by factors below)
    Rent or own status
    Crime rating
    Education rating
    Distance to business center
    """

    def get_price(self):
        return self.time_remaining

    def get_income(self):
        return self.income

    def get_price_point(self):
        return self.price_point

    def __init__(self, price, status, crime, education, distance):
        self.price = price
        self.status = status
        self.crime = crime
        self.education = education
        self.distance = distance
