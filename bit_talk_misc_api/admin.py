from django.contrib import admin
from bit_talk_misc_api.models import EmailSubscribe


class EmailSubscribeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmailSubscribe._meta.get_fields()]


admin.site.register(EmailSubscribe, EmailSubscribeAdmin)
