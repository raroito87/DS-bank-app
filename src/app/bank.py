import app


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.transactions = []

    def open_account(self, account):
        assert type(account) == app.Account, 'Account should be an app.Account'
        assert account.number not in self.accounts, 'Account number ' + str(account.number) + ' already taken!'
        self.accounts[account.number] = account
        return account

    def add_transaction(self, *, sender, recipient, subject, amount):
        assert self._is_account_number_registered(sender.number), 'Sender has no account yet!'
        assert self._is_account_number_registered(recipient.number), 'Recipient has no account yet!'
        assert sender.has_funds_for(amount), 'Account has not enough funds'
        sender.subtract_from_balance(amount)
        recipient.add_to_balance(amount)
        self.transactions.append(app.Transaction(sender=sender.number, recipient=recipient.number, subject=subject, amount=amount))
        return self.transactions[-1]

    def _is_account_number_registered(self, number):
        return number in self.accounts
