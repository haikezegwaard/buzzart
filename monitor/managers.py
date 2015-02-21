from django.db import models
import monitor.models as monitor_models

class AccountManager(models.Manager):

    def get_account_members(self, account, role="owner"):
        return self.filter(account=account, role=role).all()