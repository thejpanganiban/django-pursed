from test_utils import WalletTestCase
from errors import InsufficientBalance

# Create your tests here.


class BalanceTestCase(WalletTestCase):

    def test_default_balance(self):
        self.assertEqual(self.wallet.current_balance, 0)


class DepositTestCase(WalletTestCase):
    
    def test_deposit(self):
        """Test the basic wallet deposit operation."""
        DEPOSIT = 100
        self.wallet.deposit(DEPOSIT)

        # The wallet's current_balance should also reflect
        # the deposit's value.
        self.assertEqual(self.wallet.current_balance, DEPOSIT)

        # When I create a deposit, the wallet should create
        # a transaction equal to the value of the deposit.
        self.assertEqual(self.wallet.transaction_set.first().value, DEPOSIT)


class WithdrawTestCase(WalletTestCase):

    def test_withdraw(self):
        """Test the basic wallet withdraw operation on a
        wallet that has an initial balance."""
        INITIAL_BALANCE = 100
        self._create_initial_balance(INITIAL_BALANCE)

        WITHDRAW = 99
        self.wallet.withdraw(WITHDRAW)

        # Test that the wallet's current_balance that it
        # matches the wallet's initial balance - the
        # withdrawn amount.
        self.assertEqual(self.wallet.current_balance,
                INITIAL_BALANCE - WITHDRAW)

        # When a withdraw transaction succeeds, a
        # transaction will be created and it's value should
        # match the withdrawn value (as negative).
        self.assertEqual(self.wallet.transaction_set.last().value, -WITHDRAW)

    def test_no_balance_withdraw(self):
        """Test the basic wallet withdraw operation on a
        wallet without any transaction.
        """
        with self.assertRaises(InsufficientBalance):
            self.wallet.withdraw(100)
