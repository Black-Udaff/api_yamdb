from django.db import models

# Create your models here.
class Title(models.Model):
    name = models.TextField()
    # pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='posts'
    # )
    # # image = models.ImageField(upload_to='posts/', null=True, blank=True)
    # group = models.ForeignKey(
    #     Group,
    #     on_delete=models.SET_NULL,
    #     related_name='posts',
    #     blank=True,
    #     null=True,
    # )
    year = models.IntegerField()
    
    def __str__(self):
        return self.text
