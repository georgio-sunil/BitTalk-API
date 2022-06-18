from djongo import models


class EmailSubscribe(models.Model):
    class Meta:
        verbose_name_plural = "EmailSubscribers"

    _id = models.ObjectIdField()
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=True)
    subscription_date = models.DateField(auto_now_add=True)
