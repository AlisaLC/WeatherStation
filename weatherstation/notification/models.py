from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage

# Create your models here.
class Email(models.Model):
    recipient = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def send(self):
        email = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.recipient],
            attachments=[(attachment.name, attachment.attachment.read(), attachment.mimetype) for attachment in self.emailattachment_set.all()]
        )
        email.send()
        

class EmailAttachment(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    attachment = models.FileField(upload_to='attachments/')
    mimetype = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)