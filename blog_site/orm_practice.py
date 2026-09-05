import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_site.settings")
django.setup()

from django.db import connection, reset_queries
from django.db.models import Q, F, Count, Avg
from blog.models import Post, Category, Comment


def run():
    print("\n1. all posts")
    for p in Post.objects.all():
        print(p)

    print("\n2. filter published posts")
    for p in Post.objects.filter(status="published"):
        print(p)

    print("\n3. exclude draft posts")
    for p in Post.objects.exclude(status="draft"):
        print(p)

    print("\n4. get one post by title, and DoesNotExist")
    post = Post.objects.get(title="Django Models 101")
    print(post)
    try:
        Post.objects.get(title="Does Not Exist")
    except Post.DoesNotExist:
        print("caught Post.DoesNotExist")

    print("\n5. first, count, exists")
    print(Post.objects.first())
    print(Post.objects.count())
    print(Post.objects.filter(status="draft").exists())

    print("\n6. order_by and slicing, newest 2 posts")
    for p in Post.objects.order_by("-created_at")[:2]:
        print(p)

    print("\n7. field lookups: icontains, gte, isnull")
    for p in Post.objects.filter(title__icontains="python"):
        print(p)
    for p in Post.objects.filter(views__gte=0):
        print(p)
    for c in Comment.objects.filter(author_name__isnull=False):
        print(c)

    print("\n8. traversing relations in a lookup")
    for c in Comment.objects.filter(post__title__icontains="python"):
        print(c)

    print("\n9. Q objects for OR")
    for p in Post.objects.filter(Q(status="draft") | Q(title__icontains="venv")):
        print(p)

    print("\n10. __in lookup across a many to many relation")
    for p in Post.objects.filter(categories__name__in=["Python", "SQL"]).distinct():
        print(p)

    print("\n11. related_name reverse lookups")
    for c in post.comments.all():
        print(c)
    python_cat = Category.objects.get(name="Python")
    for p in python_cat.posts.all():
        print(p)

    print("\n12. F expressions, annotate vs aggregate")
    Post.objects.filter(title="Django Models 101").update(views=F("views") + 1)
    print(Post.objects.get(title="Django Models 101").views)

    annotated = Post.objects.annotate(comment_count=Count("comments"))
    for p in annotated:
        print(p.title, p.comment_count)

    print(Post.objects.aggregate(avg_views=Avg("views")))

    print("\nn plus 1 problem")
    reset_queries()
    for c in Comment.objects.all():
        print(c.author_name, c.post.title)
    print(f"queries used without select_related: {len(connection.queries)}")

    print("\nfixed with select_related")
    reset_queries()
    for c in Comment.objects.select_related("post").all():
        print(c.author_name, c.post.title)
    print(f"queries used with select_related: {len(connection.queries)}")


if __name__ == "__main__":
    run()
