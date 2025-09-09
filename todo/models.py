from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=200)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.title