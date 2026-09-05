import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_site.settings")
django.setup()

from blog.models import Post, Category, Comment


def seed():
    Comment.objects.all().delete()
    Post.objects.all().delete()
    Category.objects.all().delete()

    python_cat = Category.objects.create(name="Python")
    django_cat = Category.objects.create(name="Django")
    sql_cat = Category.objects.create(name="SQL")

    post1 = Post.objects.create(
        title="Learning Python OOP",
        body="Classes and objects are fun",
        status="published",
    )
    post1.categories.add(python_cat)

    post2 = Post.objects.create(
        title="Django Models 101",
        body="Fields and migrations",
        status="published",
    )
    post2.categories.add(django_cat, python_cat)

    post3 = Post.objects.create(
        title="SQL Joins Explained",
        body="Inner join vs left join",
        status="draft",
    )
    post3.categories.add(sql_cat)

    post4 = Post.objects.create(
        title="Getting Started With venv",
        body="Isolating your project",
        status="published",
    )

    Comment.objects.create(post=post1, author_name="Venu", body="Nice explanation")
    Comment.objects.create(post=post1, author_name="Sravya", body="This helped a lot")
    Comment.objects.create(post=post2, author_name="Kiran", body="Waiting for more")
    Comment.objects.create(post=post3, author_name="Nikhil", body="Left join clicked for me now")

    print("seed data created")


if __name__ == "__main__":
    seed()
