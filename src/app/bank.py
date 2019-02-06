class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []
        self.transactions = []

    def open_account(self, account):
        numbers = [item['number'] for item in self.accounts] 
        #for item in self.accounts:
            #numbers.append(item['number'])
        assert account['number'] not in numbers, 'Account number 1 already taken!'
        self.accounts.append(account)
        return account

    def add_transaction(self, *, sender, recipient, subject, amount):
        assert sender in self.accounts, 'Sender has no account yet!'
        assert recipient in self.accounts, 'Recipient has no account yet!'
        assert amount > 0, 'Amount has to be greater than 0'
        transaction = (sender, recipient, subject, amount)#tuple is no changeable, more secure
        self.transactions.append(transaction)
        return transaction
