import unittest

import app


class TestBankInitialization(unittest.TestCase):
    def test_open_account(self):
        bank = app.Bank('GLS')

        bank.open_account(account_id=1,
                          firstname='Albert',
                          lastname='Einstein')

        # Expect self.accounts to have 1 row (a length of 1)
        self.assertEqual(len(bank.accounts), 1)

        # Expect self.accounts first row to have the right values
        self.assertEqual(list(bank.accounts.iloc[0]), [1, 'Albert', 'Einstein', 0.0])

    def test_open_multiple_accounts(self):
        bank = app.Bank('GLS')

        bank.open_account(account_id=1,
                          firstname='Albert',
                          lastname='Einstein',
                          balance=100.)

        bank.open_account(account_id=2,
                          firstname='Paul',
                          lastname='Ehrenfest',
                          balance=55.5)

        self.assertEqual(len(bank.accounts), 2)
        self.assertEqual(list(bank.accounts.iloc[0]), [1, 'Albert', 'Einstein', 100.0])
        self.assertEqual(list(bank.accounts.iloc[1]), [2, 'Paul', 'Ehrenfest', 55.5])

    def test_open_account_should_return_accounts_dataframe(self):
        bank = app.Bank('GLS')

        # open_account should return the new dataframe accounts
        accounts = bank.open_account(account_id=1,
                                     firstname='Albert',
                                     lastname='Einstein',
                                     balance=100.)

        self.assertTrue(bank.accounts.equals(accounts))

    # Extra Task
    def test_open_account_number_needs_to_be_unique(self):
        bank = app.Bank('GLS')

        # Hint: Filter the accounts id column and check the lenght of the returning dataframe to be 0

        # Add an account
        bank.open_account(account_id=1,
                          firstname='Albert',
                          lastname='Einstein',
                          balance=100.)

        message = 'Account number 1 already taken!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.open_account(account_id=1,
                              firstname='Paul',
                              lastname='Ehrenfest',
                              balance=55.5)

        # Only one account entry is saved in accounts
        self.assertEqual(len(bank.accounts), 1)
