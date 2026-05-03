from django.db import models
from .consts import MAX_RATE

RATE_CHOICES = [(i, str(i)) for i in range(0, MAX_RATE + 1)]


#class SampleModel(models.Model):
#    title = models.CharField(max_length=100)
#    number = models.IntegerField()

CATEGOY = (
    ('business', 'ビジネス'),
    ('Non Fiction', 'ノンフィクション'),
    ('Fantasy', 'ファンタジー'),
    ('Mistery', 'ミステリー'),
    ('Romanse', 'ロマンス')
        )

class Book(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGOY)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '本のデータ'


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    thumbnail = models.ImageField(null=True, blank=True)
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'レビューのデータ'

