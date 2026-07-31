from datetime import timedelta
from django.utils import timezone
from .models import Job
from .models import Job, SearchCache


CACHE_DURATION = timedelta(hours=1)


def cache_valid(query=None):
    """
    Returns True if recent active jobs exist.
    """

    latest = Job.objects.filter(
        is_active=True
    ).order_by("-last_seen").first()

    if not latest:
        return False

    return (timezone.now() - latest.last_seen) < CACHE_DURATION


from django.db.models import Q

def get_cached_jobs(query):

    return Job.objects.filter(
        is_active=True
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(location__icontains=query)
    ).order_by("-last_seen")
from datetime import timedelta
from django.utils import timezone

CACHE_TIME = timedelta(hours=1)


from django.db.models import Q
from django.utils import timezone

def query_cache_valid(query):

    try:
        cache = SearchCache.objects.get(
            query=query.lower()
        )

    except SearchCache.DoesNotExist:
        return False

    # Cache expired
    if (timezone.now() - cache.last_updated) >= CACHE_TIME:
        return False

    # Cache has no matching jobs
    if not Job.objects.filter(
        is_active=True
    ).filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(location__icontains=query)
    ).exists():
        return False

    return True

def update_query_cache(query):

    SearchCache.objects.update_or_create(
        query=query.lower()
    )