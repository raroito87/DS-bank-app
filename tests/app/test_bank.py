import unittest
import app
import math
import uuid
from datetime import datetime


class TestBank(unittest.TestCase):
    def test_bank_can_be_initialized(self):
        bank = app.Bank('GLS')
        self.assertTrue(type(bank) == app.Bank)
        self.assertEqual(bank.name, 'GLS')
        self.assertEqual(bank.accounts, {})
        self.assertEqual(bank.transactions, [])

    def test_open_account(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, {})

        # Add an account
        account = app.Account(number=1,
                              firstname='Albert',
                              lastname='Einstein')

        bank.open_account(account)

        self.assertEqual(len(bank.accounts), 1)
        self.assertEqual(bank.accounts[1], account)

    def test_open_account_account_needs_to_be_app_account(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, {})

        # Add an account
        account = {
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        }

        message = 'Account should be an app.Account'
        with self.assertRaisesRegex(AssertionError, message):
            bank.open_account(account)

        # No account entry saved
        self.assertEqual(bank.accounts, {})

    def test_open_account_number_needs_to_be_unique(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, {})

        # Add an account
        account = app.Account(number=1,
                              firstname='Albert',
                              lastname='Einstein')
        bank.open_account(account)

        message = 'Account number 1 already taken!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.open_account(account)

        # Only one account entry is saved in accounts
        self.assertEqual(len(bank.accounts), 1)

    def test_open_account_should_return_account(self):
        bank = app.Bank('GLS')

        # Add an account
        account = app.Account(number=1,
                              firstname='Albert',
                              lastname='Einstein')
        einstein = bank.open_account(account)

        self.assertEqual(einstein, account)

    def test_add_transaction(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        transaction = bank.add_transaction(sender=einstein,
                                           recipient=ehrenfest,
                                           subject='Bücher',
                                           amount=100.0)

        self.assertEqual(len(bank.transactions), 1)
        self.assertEqual(bank.transactions, [transaction])

    def test_add_transaction_with_zero_or_negative_amount(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        message = 'Amount needs to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=0.0)

        message = 'Amount needs to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=-100.0)

        # No transaction is saved
        self.assertEqual(bank.transactions, [])

    def test_add_transaction_with_invalid_sender(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        # Just the account
        einstein = app.Account(**{
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
            'balance': 500.0
        })

        # Add account
        ehrenfest = bank.open_account(
            app.Account(**{
                'number': 2,
                'firstname': 'Paul',
                'lastname': 'Ehrenfest',
            })
        )

        message = 'Sender has no account yet!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=100.0)

    def test_add_transaction_with_invalid_recipient(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        # Add account
        einstein = bank.open_account(
            app.Account(**{
                'number': 1,
                'firstname': 'Albert',
                'lastname': 'Einstein',
                'balance': 500.0
            })
        )

        # Just the account
        ehrenfest = app.Account(**{
            'number': 2,
            'firstname': 'Paul',
            'lastname': 'Ehrenfest',
        })

        message = 'Recipient has no account yet!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=100.0)

    # Extra Task
    def test_add_transaction_changes_sender_balance(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        transaction = bank.add_transaction(sender=einstein,
                                           recipient=ehrenfest,
                                           subject='Bücher',
                                           amount=100.0)

        self.assertEqual(einstein.balance, 400.0)
        self.assertEqual(len(bank.transactions), 1)
        self.assertEqual(bank.transactions, [transaction])

    def test_add_transaction_changes_recipient_balance(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=500.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        transaction = bank.add_transaction(sender=einstein,
                                           recipient=ehrenfest,
                                           subject='Bücher',
                                           amount=100.0)

        self.assertEqual(ehrenfest.balance, 100.0)
        self.assertEqual(len(bank.transactions), 1)
        self.assertEqual(bank.transactions, [transaction])

    def test_add_transaction_with_insufficient_funds(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account(
            app.Account(number=1,
                        firstname='Albert',
                        lastname='Einstein',
                        balance=50.0)
        )
        ehrenfest = bank.open_account(
            app.Account(number=2,
                        firstname='Paul',
                        lastname='Ehrenfest')
        )

        message = 'Account has not enough funds'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=einstein,
                                 recipient=ehrenfest,
                                 subject='Bücher',
                                 amount=100.0)

        self.assertEqual(einstein.balance, 50.0)
        self.assertEqual(ehrenfest.balance, 0.0)
        self.assertEqual(bank.transactions, [])

    def test_obtain_account_statement(self):
        bank = self._create_bank_with_100_accounts_different_balances()

        self.assertEqual(len(bank.accounts), 100)

        self._add_transactions_to_Bank(bank, 200, '2019', '01')
        self._add_transactions_to_Bank(bank, 200, '2019', '08')
        self._add_transactions_to_Bank(bank, 200, '2020', '03')

        self.assertEqual(len(bank.transactions), 600)

        init_year = 2019
        init_month = 1

        # only one month
        account_statement = bank.get_account_statement(account_number=1, init_year=init_year, init_month=init_month)
        self.assertEqual(len(account_statement), 4)

        # from january to october
        final_year = 2019
        final_month = 10
        account_statement = bank.get_account_statement(account_number=1, init_year=init_year, init_month=init_month,
                                                       final_year=final_year, final_month=final_month)
        self.assertEqual(len(account_statement), 8)

    def test_obtain_transaction_categories(self):
        bank = self._create_bank_with_100_accounts_different_balances()

        self.assertEqual(len(bank.accounts), 100)

        self._add_transactions_to_Bank(bank, 200, '2019', '01', app.TransactionCategory.UNKNOWN)
        self._add_transactions_to_Bank(bank, 100, '2019', '01', app.TransactionCategory.SEX)
        self._add_transactions_to_Bank(bank, 50, '2019', '01', app.TransactionCategory.DRUGS)

        self.assertEqual(len(bank.get_unkown_transactions()), 200)
        self.assertEqual(len(bank.get_sex_transactions()), 100)
        self.assertEqual(len(bank.get_drugs_transactions()), 50)
        self.assertEqual(len(bank.get_rockandroll_transactions()), 0)

    def test_transaction_id_is_unique(self):
        bank = self._create_bank_with_100_accounts_different_balances()

        self.assertEqual(len(bank.accounts), 100)

        self._add_transactions_to_Bank(bank, 200, '2019', '01')
        self._add_transactions_to_Bank(bank, 200, '2019', '08')
        self._add_transactions_to_Bank(bank, 200, '2020', '03')

        self.assertEqual(len(bank.transactions), 600)

        dict_id = {}
        for t in bank.transactions:
            dict_id[t.transactionID] = ''

        #  all the id are different, no key repeated
        self.assertEqual(len(bank.transactions), len(dict_id))


    def _create_bank_with_100_accounts_different_balances(self):
        bank = app.Bank('DKB')

        firstname = 'Rafael'
        lastname = 'Rodriguez'
        for idx in range(0, 100):
            bank.open_account(app.Account(firstname=firstname + str(idx), lastname=lastname + str(idx), number=idx,
                                          balance=1000.0 + 10*idx))

        return bank

    def _add_transactions_to_Bank(self, bank, number_of_transactions, year, month, category=app.TransactionCategory.UNKNOWN):
        assert type(year) == str
        assert type(month) == str
        assert type(number_of_transactions) == int and number_of_transactions > 0
        assert len(bank.accounts) > 1  # at least 2 accounts to generate transfers

        for sender_index in range (0, number_of_transactions):
            recipient_index = sender_index + 1  #
            sender_index = int(math.fmod(sender_index, len(bank.accounts)))
            recipient_index = int(math.fmod(recipient_index, len(bank.accounts)))
            transaction = bank.add_transaction(sender=bank.accounts[sender_index], recipient=bank.accounts[recipient_index],
                                               subject='pocketmoney', amount=10 + sender_index/2,
                                               category=category)

            transaction.transactionID = year + month + datetime.now().strftime('%d%H%M%S') + '_' + str(uuid.uuid4())# this month
