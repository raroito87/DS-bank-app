import app


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.transactions = []

    def open_account(self, account):
        assert type(account) == app.Account, 'Account should be an app.Account'
        #  assert account.number not in self.accounts, 'Account number ' + str(account.number) + ' already taken!'
        assert not self._is_account_number_registered(account.number), 'Account number ' + str(account.number) + ' already taken!'
        self.accounts[account.number] = account
        return account

    def add_transaction(self, *, sender, recipient, subject, amount, category=None):
        assert self._is_account_number_registered(sender.number), 'Sender has no account yet!'
        assert self._is_account_number_registered(recipient.number), 'Recipient has no account yet!'
        assert sender.has_funds_for(amount), 'Account has not enough funds'
        sender.subtract_from_balance(amount)
        recipient.add_to_balance(amount)
        self.transactions.append(app.Transaction(sender=sender.number, recipient=recipient.number, subject=subject, amount=amount, category=category))
        return self.transactions[-1]

    def _is_account_number_registered(self, number):
        return number in self.accounts

    def get_account_statement(self, *, account_number, init_year, init_month, final_year=None, final_month=None):
        return self._get_transactions_from_account(account_number, self._get_transactions_between(init_year, init_month, final_year, final_month))

    def _get_transactions_between(self, init_year, init_month, final_year, final_month):
        assert init_year > 2018, 'Initial year not valid!'
        assert 0 < init_month < 13, 'Initial month not valid!'

        #  if final year is not given we use the initial date as final date -> transaction of only a month
        if final_year:
            assert final_year > 2018, 'Final year not valid!'
            assert 0 < final_month < 13, 'Final month not valid!'
        else:
            final_year = init_year
            final_month = init_month

        init_date_id = init_year*100+init_month
        final_date_id = final_year*100+final_month

        fetched_transactions = []
        for t in self.transactions:
            if init_date_id <= t.get_year_month() <= final_date_id:
                fetched_transactions.append(t)

        return fetched_transactions

    def _get_transactions_from_account(self, account_number, transactions_list):
        assert self._is_account_number_registered(account_number), 'Account is not registered'
        assert len(transactions_list) > 0, 'transactions list is empty!'

        fetched_transactions = []
        for t in transactions_list:
            if t.sender == account_number or t.recipient == account_number:
                fetched_transactions.append(t)

        return fetched_transactions

    def _get_category_transactions(self, category):
        transtactions_category = []
        for t in self.transactions:
            if t.category == category:
                transtactions_category.append(t)

        return transtactions_category

    def get_sex_transactions(self):
        return self._get_category_transactions(app.TransactionCategory.SEX)

    def get_drugs_transactions(self):
        return self._get_category_transactions(app.TransactionCategory.DRUGS)

    def get_rockandroll_transactions(self):
        return self._get_category_transactions(app.TransactionCategory.RockAndRoll)

    def get_unkown_transactions(self):
        return self._get_category_transactions(app.TransactionCategory.UNKNOWN)







