def calculate_achievements(
    resume,
    applications_count,
    placement_score,
    saved_jobs_count
):

    achievements = []

    if resume:
        achievements.append(
            "📄 Resume Uploaded"
        )

    if placement_score >= 80:
        achievements.append(
            "🏆 Resume Score Above 80"
        )

    if applications_count >= 1:
        achievements.append(
            "💼 First Job Application"
        )

    if applications_count >= 10:
        achievements.append(
            "🚀 Applied to 10 Jobs"
        )

    if saved_jobs_count >= 5:
        achievements.append(
            "⭐ Saved 5 Jobs"
        )

    if placement_score >= 90:
        achievements.append(
            "🥇 Placement Ready"
        )

    return achievements