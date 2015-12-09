django-pursed
===

A simple wallet django app.

Usage
---

### Creating a New Wallet

```python
from wallet.models import Wallet

# wallets are owned by users.
wallet = user.wallet_set.create()
```

### Despositing a balance to a wallet

```python
from django.db import transaction

with transaction.atomic():
    # We need to lock the wallet first so that we're sure
    # that nobody modifies the wallet at the same time 
    # we're modifying it.
    wallet = Wallet.select_for_update().get(pk=wallet.id)
    wallet.deposit(100)  # amount
    wallet.save()
```

### Withdrawing a balance from a wallet

```python
from django.db import transaction

with transaction.atomic():
    # We need to lock the wallet first so that we're sure
    # that nobody modifies the wallet at the same time 
    # we're modifying it.
    wallet = Wallet.select_for_update().get(pk=wallet.id)
    wallet.withdraw(100)  # amount
    wallet.save()
```

### Withdrawing with an insufficient balance

When a user tries to withdraw from a wallet with an amount
greater than its balance, the transaction raises a
`wallet.errors.InsufficientBalance` error.

```python
# wallet.current_balance  # 50

# This raises an wallet.errors.InsufficentBalance.
wallet.withdraw(100)
```

This error inherits from `django.db.IntegrityError` so that
when it is raised, the whole transaction is automatically
rolled-back.
