from django.db import models

# Create your models here.


CATEGORY_CHOICES = [
    ('Anime', 'Anime'),
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Horror', 'Horror'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Documentary', 'Documentary'),
    ('Animation', 'Animation'),
    ('Thriller', 'Thriller'),
    ('Romance', 'Romance'),
    ('Fantasy', 'Fantasy'),
]


class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail_url = models.FileField(upload_to='thumbnails/', blank=True, null=True)
    category= models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Action')
    video_file = models.FileField(upload_to='video/', blank=False, null=False)



    def __str__(self):
        return self.title