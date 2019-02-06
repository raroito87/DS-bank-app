class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = []
        self.transactions = []

    def open_account(self, account):
        numbers = [item['number'] for item in self.accounts]
        assert account['number'] not in numbers, 'Account number 1 already taken!'
        self.accounts.append(account)
        return account

    def add_transaction(self, *, sender, recipient, subject, amount):
        assert sender in self.accounts, 'Sender has no account yet!'
        assert recipient in self.accounts, 'Recipient has no account yet!'
        assert amount > 0, 'Amount has to be greater than 0'
        transaction = (sender, recipient, subject, amount)
        self.transactions.append(transaction)
        return transaction

    def _print_info_account(self, account):
        print('account number', account['number'], ' / ', account['firstname'], ' ', account['lastname'])

    def print_info_accounts(self):
        print('number od accounts', len(self.accounts))
        for account in self.accounts:
            self._print_info_account(account)

    def _print_info_transaction(self, transaction):
        print('sender #: ', transaction[0]['number'], ' to recipient #: ' , transaction[1]['number'], ', subject: ', transaction[2], ', amount: ', transaction[3])

    def print_info_transactions(self):
        print('number of transactions performed: ', len(self.transactions))
        for transaction in self.transactions:
            self._print_info_transaction(transaction)
