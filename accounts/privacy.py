from accounts.models import StudentProfile


def can_view_resume(owner, viewer):

    profile = StudentProfile.objects.get(
        user=owner
    )

    # Owner can always view
    if owner == viewer:
        return True

    # Public
    if profile.resume_visibility == "public":
        return True

    # Recruiters Only
    if profile.resume_visibility == "recruiters":
        return getattr(viewer, "is_recruiter", False)

    # Private
    return False


def can_view_portfolio(owner, viewer):

    profile = StudentProfile.objects.get(
        user=owner
    )

    # Owner can always view
    if owner == viewer:
        return True

    # Public
    if profile.portfolio_visibility == "public":
        return True

    # Private
    return False