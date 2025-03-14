from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from PIL import Image
import uuid as u
import os
# Create your models here.

@deconstructible
class FileExtensionValidator:
    allowed_extensions = {'jpg', 'png'}

    def __call__(self, value):
        ext = value.name.split('.')[-1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(f"Invalid file type: {ext}. Allowed: {self.allowed_extensions}")


def upload_to(instance, filename):
    ext = filename.split('.')[-1].lower()
    new_filename = f"photo_{u.uuid4()}.{ext}"
    return os.path.join('uploads/', new_filename)


class EventModel(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=30)
    organizedby = models.ForeignKey(User, on_delete=models.CASCADE)
    coverphoto = models.ImageField(upload_to=upload_to, validators=[FileExtensionValidator()])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.coverphoto:
            self.crop_image()

    def __str__(self):
        return self.title + "url: " + self.coverphoto.url
    
    def crop_image(self):
        """Crop the uploaded image to a square (e.g., 300x300 pixels)."""
        img_path = self.coverphoto.path
        with Image.open(img_path) as img:
            width, height = img.size
            new_size = min(width, height)  # Get the shortest side
            left = (width - new_size) / 2
            top = (height - new_size) / 2
            right = (width + new_size) / 2
            bottom = (height + new_size) / 2

            img = img.crop((left, top, right, bottom))
            img = img.resize((300, 300))  # Resize to 300x300
            img.save(img_path)  # Overwrite the existing file

class AttendeeModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    registered = models.DateTimeField(auto_now_add=True)
    ticket = models.ImageField(upload_to="uploads/", null=True, validators=[FileExtensionValidator()])

    def __str__(self):
        return self.name
    

