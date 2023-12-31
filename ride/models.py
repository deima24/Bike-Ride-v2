from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models import Avg

STATUS = ((0, "Draft"), (1, "Published"))

diff = [("Moderate", "Moderate"), ("Hard", "Hard"), ("Easy", "Easy")]


class Entry(models.Model):
    """
    Storing Entry data
    """

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    distance = models.IntegerField(help_text="Add the distance", default=0)
    start = models.TextField(blank=False)
    finish = models.TextField(blank=False)
    content = models.TextField()
    featured_image = CloudinaryField("image", default="placeholder")
    status = models.IntegerField(choices=STATUS, default=0)
    difficulty = models.CharField(
        max_length=10, null=True, blank=True, choices=diff
    )

    class Meta:
        ordering = ["-created_on"]

    def average_rating(self) -> float:
        return (
            Rating.objects.filter(entry=self).aggregate(Avg("rating"))[
                "rating__avg"
            ]
            or 0
        )

    def __str__(self):
        return f"{self.title}: {self.average_rating()}"


class Comment(models.Model):
    """
    Storing the Comment data
    """

    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.entry.title}: {self.rating}"
