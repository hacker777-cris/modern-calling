from django.db import models



class Recording(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='recordings/')

    def __str__(self):
        return self.title
