from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blogapp.models import (
    Post,
    Comments,
)  # Замените `your_app` на имя вашего приложения
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = "Generates seed data for Posts and Comments"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Post.objects.all().delete()
        Comments.objects.all().delete()

        self.stdout.write("Creating users...")
        users = []
        for _ in range(5):
            user = User.objects.create_user(
                username=fake.user_name(), email=fake.email(), password="password123"
            )
            users.append(user)

        self.stdout.write("Creating posts...")
        posts = []
        for _ in range(20):
            post = Post.objects.create(
                title=fake.sentence(),
                content=fake.paragraph(),
                views=random.randint(0, 100),
                author=random.choice(users),
                date_created=fake.date_time_this_year(),
            )
            posts.append(post)

        self.stdout.write("Creating comments...")
        for _ in range(50):
            Comments.objects.create(
                post=random.choice(posts),
                author=random.choice(users),
                content=fake.paragraph(),
            )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully!"))
