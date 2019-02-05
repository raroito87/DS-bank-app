import unittest
import app


class TestBank(unittest.TestCase):
    def test_bank_can_be_initialized(self):
        bank = app.Bank('GLS')
        self.assertTrue(type(bank) == app.Bank)
        self.assertEqual(bank.name, 'GLS')
        self.assertEqual(bank.accounts, [])
        self.assertEqual(bank.transactions, [])

    def test_open_account(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, [])

        # Add an account
        account = {
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        }
        bank.open_account(account)

        self.assertEqual(len(bank.accounts), 1)
        self.assertEqual(bank.accounts, [account])

    def test_open_account_should_return_account_infos(self):
        bank = app.Bank('GLS')

        # Add an account
        account = {
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        }
        einstein = bank.open_account(account)

        self.assertEqual(einstein, account)

    # Extra Task
    def test_open_account_number_needs_to_be_unique(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.accounts, [])

        # Add an account
        account = {
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        }
        bank.open_account(account)

        message = 'Account number 1 already taken!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.open_account(account)

        # Only one account entry is saved in accounts
        self.assertEqual(bank.accounts, [account])

    def test_add_transaction(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account({
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        })
        ehrenfest = bank.open_account({
            'number': 2,
            'firstname': 'Paul',
            'lastname': 'Ehrenfest',
        })

        transaction = bank.add_transaction(sender=ehrenfest,
                                           recipient=einstein,
                                           subject='Bücher',
                                           amount=100)

        self.assertEqual(len(bank.transactions), 1)
        self.assertEqual(bank.transactions, [transaction])

    def test_add_transaction_with_zero_or_negative_amount(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        einstein = bank.open_account({
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        })
        ehrenfest = bank.open_account({
            'number': 2,
            'firstname': 'Paul',
            'lastname': 'Ehrenfest',
        })

        message = 'Amount has to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=ehrenfest,
                                 recipient=einstein,
                                 subject='Bücher',
                                 amount=0)

        message = 'Amount has to be greater than 0'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=ehrenfest,
                                 recipient=einstein,
                                 subject='Bücher',
                                 amount=-100)

        # No transaction is saved
        self.assertEqual(bank.transactions, [])

    # Extra Task
    def test_add_transaction_with_invalid_sender(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        # Add account
        einstein = bank.open_account({
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        })

        # Just the dict
        ehrenfest = {
            'number': 2,
            'firstname': 'Paul',
            'lastname': 'Ehrenfest',
        }

        message = 'Sender has no account yet!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=ehrenfest,
                                 recipient=einstein,
                                 subject='Bücher',
                                 amount=100)

    def test_add_transaction_with_invalid_recipient(self):
        bank = app.Bank('GLS')
        self.assertEqual(bank.transactions, [])

        # Just the dict
        einstein = {
            'number': 1,
            'firstname': 'Albert',
            'lastname': 'Einstein',
        }

        # Add account
        ehrenfest = bank.open_account({
            'number': 2,
            'firstname': 'Paul',
            'lastname': 'Ehrenfest',
        })

        message = 'Recipient has no account yet!'
        with self.assertRaisesRegex(AssertionError, message):
            bank.add_transaction(sender=ehrenfest,
                                 recipient=einstein,
                                 subject='Bücher',
                                 amount=100)
