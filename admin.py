from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

from django_bigbluebutton.models import Meeting, RegisteredUser


class MeetingAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    ordering = ['name']
    actions = ['send_mail_to_registered_users']

    def send_mail_to_registered_users(self, request, queryset):
        for meeting in queryset.filter():
            users = RegisteredUser.objects.filter(meetings=meeting.unique_id)

            mails = []

            for user in users:
                mails.append(user.mail)

            subject = _('Informations sur la conférence : ') + meeting.name
            content = _('''La conférence ouvrira dans moins 24h, le mot de passe pour y accéder est le suivant : ''') + meeting.attendee_pw

            send_mail(subject, content, settings.EMAIL_HOST_USER,
                      mails, fail_silently=False)

    send_mail_to_registered_users.short_description = _('Envoyer un mail aux participants à la(les) conférence(s) sélectionnée(s)')

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(RegisteredUser)