def remove_duplicates(jobs):
    """
    Remove duplicate jobs based on
    Title + Company + Location.
    """

    unique_jobs = []
    seen = set()

    for job in jobs:

        key = (
            job.get("title", "").strip().lower(),
            job.get("company", "").strip().lower(),
            job.get("location", "").strip().lower(),
        )

        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)

    return unique_jobs