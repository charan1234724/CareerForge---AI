from .adzuna import search_adzuna
# from .jooble import search_jooble
# from .indianapi import search_indianapi

from .merge_engine import merge_jobs
from .duplicate_engine import remove_duplicates


def search_jobs(query, page=1):
    adzuna = search_adzuna(query, page)

    # jooble = search_jooble(query, page)
    # indian = search_indianapi(query, page)

    jobs = merge_jobs(
        adzuna,
        [],      # placeholder for Jooble
        []       # placeholder for IndianAPI
    )

    return remove_duplicates(jobs)