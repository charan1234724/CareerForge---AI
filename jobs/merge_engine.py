def normalize_adzuna(data):
    """
    Convert Adzuna response into a common job format.
    """

    jobs = []

    for job in data.get("results", []):

        jobs.append({
            "id": job.get("id"),

            "title": job.get("title"),

            "company": (
                job.get("company", {}) or {}
            ).get("display_name", "Unknown"),

            "location": (
                job.get("location", {}) or {}
            ).get("display_name", ""),

            "description": job.get("description"),

            "salary_min": job.get("salary_min"),

            "salary_max": job.get("salary_max"),

            "url": job.get("redirect_url"),

            "source": "Adzuna",
        })

    return jobs


def normalize_jooble(data):
    """
    Convert Jooble response into a common job format.
    """

    jobs = []

    for job in data.get("jobs", []):

        jobs.append({
            "id": job.get("id"),

            "title": job.get("title"),

            "company": job.get("company", "Unknown"),

            "location": job.get("location", ""),

            "description": job.get("snippet"),

            "salary_min": None,

            "salary_max": None,

            "url": job.get("link"),

            "source": "Jooble",
        })

    return jobs


def normalize_indianapi(data):
    """
    Convert IndianAPI response into the common format.
    Safe placeholder until the API is available.
    """

    jobs = []

    for job in data.get("jobs", []):

        jobs.append({
            "id": job.get("id"),

            "title": job.get("title"),

            "company": job.get("company", "Unknown"),

            "location": job.get("location", ""),

            "description": job.get("description"),

            "salary_min": job.get("salary_min"),

            "salary_max": job.get("salary_max"),

            "url": job.get("url"),

            "source": "IndianAPI",
        })

    return jobs


def merge_jobs(
    adzuna_data,
    jooble_data=None,
    indianapi_data=None,
):
    """
    Merge jobs from all providers.
    """

    jobs = []

    if adzuna_data:
        jobs.extend(normalize_adzuna(adzuna_data))

    if jooble_data:
        jobs.extend(normalize_jooble(jooble_data))

    if indianapi_data:
        jobs.extend(normalize_indianapi(indianapi_data))

    return jobs