from datetime import datetime
from enum import Enum
import uuid


class TransactionCategory(Enum):
    UNKNOWN = 0
    SEX = 1
    DRUGS = 2
    RockAndRoll = 3


class Transaction():
    def __init__(self, *, sender, recipient, subject, amount, category=None):
        assert type(sender) == int, 'Sender needs to be an integer'
        assert type(recipient) == int, 'Recipient needs to be an integer'
        assert type(amount) == float, 'Amount needs to be a float'
        assert amount > 0.0, 'Amount needs to be greater than 0'
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.amount = amount
        self.transactionID = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + str(uuid.uuid4())
        if category:
            self.category = category
        else:
            self.category = TransactionCategory.UNKNOWN


    # def info(self):
    #     return 'From ' + str(self.sender) + ' to ' + str(self.recipient) + ': ' + self.subject + ' - ' + str(self.amount) + ' €'

    def info(self):
        return 'From {} to {}: {} - {} €'.format(self.sender, self.recipient, self.subject, self.amount)

    def get_year_month(self):
        return self._get_year()*100 + self._get_month()

    def _get_year(self):
        return int(self.transactionID[0:4])

    def _get_month(self):
        return int(self.transactionID[4:6])

    def _get_day(self):
        return int(self.transactionID[6:8])

    def _get_hour(self):
        return int(self.transactionID[8:10])

    def _get_minute(self):
        return int(self.transactionID[10:12])

    def _get_second(self):
        return int(self.transactionID[12:14])
