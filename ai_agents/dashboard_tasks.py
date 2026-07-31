def generate_daily_tasks(placement):

    tasks = []

    if placement["ats"] < 80:

        tasks.append(
            "Improve ATS keywords in your resume."
        )

    if placement["resume"] < 80:

        tasks.append(
            "Strengthen projects and achievements."
        )

    if placement["applications"] < 60:

        tasks.append(
            "Apply to at least 5 jobs today."
        )

    if placement["interview"] < 80:

        tasks.append(
            "Complete one mock interview."
        )

    if placement["score"] >= 80:

        tasks.append(
            "Keep applying consistently."
        )

    return tasks