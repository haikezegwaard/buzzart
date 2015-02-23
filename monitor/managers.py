from django.db import models


class AccountManager(models.Manager):

    def get_account_members(self, account, role="owner"):
        return self.filter(account=account, role=role).all()
