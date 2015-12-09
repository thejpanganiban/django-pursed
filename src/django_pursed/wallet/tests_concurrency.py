from django.db import transaction
from models import Wallet
from test_utils import WalletTestCase
import threading
import time


class ConcurrentDepositTestCase(WalletTestCase):

    def test_deposit(self):
        """Test two concurrent deposit transactions."""
        DEPOSIT = 100

        def deposit_thread():
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(
                        pk=self.wallet.id)
                wallet.deposit(DEPOSIT)

                # We simulate a long transaction so that
                # when the other thread comes in, this
                # thread still holds the lock.
                time.sleep(1)

        # We run the two threads to simulate two
        # transactions running simultaneously.
        t1 = threading.Thread(target=deposit_thread)
        t2 = threading.Thread(target=deposit_thread)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # We retrieve a new wallet object since what we
        # currently have is now stale.
        wallet = Wallet.objects.get(pk=self.wallet.id)

        # We check that the current_balance wasn't
        # overwritten by the other transaction. In short,
        # we should get the correct deposited total amount.
        self.assertEqual(wallet.current_balance, DEPOSIT * 2)

        # We then check that we have two transactions. Each
        # having the deposited amount.
        self.assertEqual(wallet.transaction_set.count(), 2)

    def test_withdraw(self):
        """Test two concurrent withdraw transactions."""
        INITIAL_BALANCE = 200
        self._create_initial_balance(INITIAL_BALANCE)
        WITHDRAW = 100

        def withdraw_thread():
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(
                        pk=self.wallet.id)
                wallet.withdraw(WITHDRAW)

                # We simulate a long transaction so that
                # when the other thread comes in, this
                # thread still holds the lock.
                time.sleep(1)

        t1 = threading.Thread(target=withdraw_thread)
        t2 = threading.Thread(target=withdraw_thread)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        wallet = Wallet.objects.get(pk=self.wallet.id)

        # Assert that both transactions were able to
        # succeed.
        self.assertEqual(wallet.current_balance,
                INITIAL_BALANCE - (WITHDRAW * 2))

        # We also check that the number of transactions
        # created only equates to the number of
        # transactions successful + the initial transaction.
        self.assertEqual(wallet.transaction_set.count(), 3)

    def test_multiple_withdraw_insufficient_balance(self):
        """We're going to test two concurrent withdraw
        transactions happening in parallel where one would
        end-up with an insufficient balance."""
        INITIAL_BALANCE = 199
        self._create_initial_balance(INITIAL_BALANCE)
        WITHDRAW = 100

        def withdraw_thread():
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(
                        pk=self.wallet.id)
                wallet.withdraw(WITHDRAW)

                # We simulate a long transaction so that
                # when the other thread comes in, this
                # thread still holds the lock.
                time.sleep(1)

        t1 = threading.Thread(target=withdraw_thread)
        t2 = threading.Thread(target=withdraw_thread)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        wallet = Wallet.objects.get(pk=self.wallet.id)

        # Assert that the only the first transaction was
        # able to succeed by checking that only one
        # transaction's value was applied.
        self.assertEqual(wallet.current_balance,
                INITIAL_BALANCE - (WITHDRAW * 1))

        # We also check that the number of transactions
        # created only equates to the number of
        # transactions successful + the initial transaction.
        self.assertEqual(wallet.transaction_set.count(), 2)


class ConcurrentTransferTestCase(WalletTestCase):

    def test_transfer(self):
        """We're going to simulate concurrent transfer to a
        single wallet."""
        INITIAL_BALANCE = 200
        self._create_initial_balance(INITIAL_BALANCE)
        TRANSFER = 100

        _wallet2 = self.user.wallet_set.create()
        wallet2_id = _wallet2.id

        def transfer_thread():
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(
                        pk=self.wallet.id)
                wallet2 = Wallet.objects.select_for_update().get(pk=wallet2_id)
                wallet.transfer(wallet2, TRANSFER)

                # We simulate a long transaction so that
                # when the other thread comes in, this
                # thread still holds the lock.
                time.sleep(1)

        t1 = threading.Thread(target=transfer_thread)
        t2 = threading.Thread(target=transfer_thread)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        wallet = Wallet.objects.get(pk=self.wallet.id)
        wallet2 = Wallet.objects.get(pk=wallet2_id)

        # Assert that all transfers were made and that
        # both applies to the wallet's current_balance.
        self.assertEqual(wallet.current_balance,
                INITIAL_BALANCE - (TRANSFER * 2))
        self.assertEqual(wallet2.current_balance, TRANSFER * 2)
