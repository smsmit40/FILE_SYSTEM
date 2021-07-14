import django.forms
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import uuid
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import os

class NewFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    description = models.TextField()
    the_file = models.FileField(upload_to='media/')
    upload_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(models.signals.post_delete, sender=NewFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.the_file:
        if os.path.isfile(instance.the_file.path):
            os.remove(instance.the_file.path)

@receiver(models.signals.pre_save, sender=NewFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = NewFile.objects.get(pk=instance.pk).the_file
    except NewFile.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class FileForm(ModelForm):
    class Meta:
        model = NewFile
        fields = ['name', 'description', 'the_file']

