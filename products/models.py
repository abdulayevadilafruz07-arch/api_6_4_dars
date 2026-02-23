from django.db import models

from django.db import models



class Product(models.Model):
    brand = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.TextField()



    def __str__(self):
        return self.title

