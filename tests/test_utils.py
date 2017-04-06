from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
import logging


User = get_user_model()
logger = logging.getLogger(__name__)


class WalletTestCase(TransactionTestCase):

    def _create_initial_balance(self, value):
        self.wallet.transaction_set.create(
            value=value,
            running_balance=value
        )
        self.wallet.current_balance = value
        self.wallet.save()

    def setUp(self):
        logger.info('Creating wallet...')
        self.user = User()
        self.user.save()
        self.wallet = self.user.wallet_set.create()
        self.wallet.save()
        logger.info('Wallet created.')
