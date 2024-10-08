from django.db import models
from common.models import CommonModel


class Tweet(CommonModel):
    payload = models.CharField(max_length=180)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.user}] {self.payload}"

    def total_likes(self):
        return self.likes.count()


class Like(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="likes",
    )
    tweet = models.ForeignKey(
        "tweets.Tweet",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    def __str__(self):
        return f"{self.user} like {self.tweet.pk}"
