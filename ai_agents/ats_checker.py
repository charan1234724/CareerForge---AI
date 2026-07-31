def calculate_ats_score(text):

    score = 0

    feedback = []

    text = text.lower()

    if "skills" in text:
        score += 20
        feedback.append("✓ Skills section found")

    if "project" in text:
        score += 20
        feedback.append("✓ Projects section found")

    if "education" in text:
        score += 20
        feedback.append("✓ Education section found")

    if "github" in text:
        score += 20
        feedback.append("✓ GitHub link found")

    if "linkedin" in text:
        score += 20
        feedback.append("✓ LinkedIn profile found")

    return score, feedback