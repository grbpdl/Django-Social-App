from django.db import models
from accounts.models import User

class PostCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    content = models.TextField()
    title = models.CharField(max_length=255 )  # Recipe title
    ingredients = models.TextField(help_text="List of ingredients", blank=True, null=True)
    estimated_time = models.DurationField(blank=True, null=True, help_text="Estimated preparation time")
    servings = models.PositiveIntegerField(blank=True, null=True, help_text="Number of servings")
    difficulty = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        blank=True,
        null=True
    )
    instructions = models.TextField(help_text="Step-by-step instructions" ,null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True, help_text="Additional notes or tips")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name if self.category else 'No Category'}"


# Model to save posts by users
class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"
