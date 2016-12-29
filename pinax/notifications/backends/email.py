from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from html2text import html2text

from .base import BaseBackend


class EmailBackend(BaseBackend):
    spam_sensitivity = 2

    def can_send(self, user, notice_type, scoping):
        can_send = super(EmailBackend, self).can_send(user, notice_type, scoping)
        if can_send and user.email:
            return True
        return False

    def get_context(self, recipient, sender, notice_type, extra_context):
        context = super().get_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
        })
        context.update(extra_context)
        return context

    def get_subject(self, label, context):
        return render_to_string(
            'pinax/notifications/{}/subject.txt'.format(label), context).splitlines()

    def get_body(self, label, context):
        return render_to_string(
            'pinax/notifications/{}/body.html'.format(label), context).splitlines()

    def deliver(self, recipient, sender, notice_type, extra_context):
        context = self.get_context(recipient, sender, notice_type, extra_context)
        subject = self.get_subject(notice_type.label, context)
        body = self.get_body(notice_type.label, context)
        send_mail(subject, html2text(body), settings.DEFAULT_FROM_EMAIL,
                  [recipient.email], fail_silently=False, html_message=body)
