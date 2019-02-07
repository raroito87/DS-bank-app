class Account:
    def __init__(self, *, firstname, lastname, number, balance=0.0):
        assert type(number) == int, 'Number needs to be an integer'
        assert type(balance) == float, 'Balance needs to be a float'
        self.firstname = firstname
        self.lastname = lastname
        self.number = number
        self.balance = balance

    # def info(self):
    #     return 'Number ' + str(self.number) + ': ' + self.firstname + ' ' + self.lastname + ' - ' + str(self.balance) + ' €'

    # def info(self):
    #     return f'Number {self.number}: {self.firstname} {self.lastname} - {self.balance} €'

    def info(self):
        template = 'Number {}: {} {} - {} €'.format(self.number, self.firstname, self.lastname, self.balance)
        return template

    def has_funds_for(self, amount):
        return amount <= self.balance

    def add_to_balance(self, amount):
        assert amount > 0, 'Amount needs to be greater than 0'
        self.balance += amount

    def subtract_from_balance(self, amount):
        assert amount <= self.balance, 'Account has not enough funds'
        self.balance -= amount
