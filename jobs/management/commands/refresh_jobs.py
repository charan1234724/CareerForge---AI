from django.core.management.base import BaseCommand

from jobs.job_search import search_jobs
from jobs.sync_engine import sync_jobs, deactivate_old_jobs
from jobs.cache_engine import update_query_cache
from django.contrib.auth.models import User
from jobs.job_alerts import check_user_jobs

POPULAR_SEARCHES = [
    "python developer india",
    "java developer india",
    "full stack developer india",
    "ai engineer india",
    "machine learning engineer india",
    "data scientist india",
    "software engineer india",
]


class Command(BaseCommand):

    help = "Refresh job database"

    def handle(self, *args, **kwargs):

        self.stdout.write("Refreshing jobs...")

        for query in POPULAR_SEARCHES:

            self.stdout.write(f"Fetching: {query}")

            jobs = search_jobs(query)

            sync_jobs(jobs)
            for user in User.objects.filter(is_active=True):

                check_user_jobs(user, jobs)

            update_query_cache(query)

        deactivate_old_jobs()

        self.stdout.write(
            self.style.SUCCESS("Job refresh completed.")
        )