from django.db import IntegrityError


class InsufficientBalance(IntegrityError):
    """Raised when a wallet has insufficient balance to
    run an operation.

    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """
