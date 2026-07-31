def extract_education(text):

    keywords = [
        "b.tech",
        "btech",
        "engineering",
        "college",
        "university",
        "degree",
        "intermediate",
        "ssc",
        "education"
    ]

    results = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        for keyword in keywords:

            if keyword in line.lower():

                results.append(line)

                break

    return list(dict.fromkeys(results))


def extract_projects(text):

    keywords = [
        "project",
        "developed",
        "built",
        "created",
        "designed",
        "implementation"
    ]

    projects = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        for keyword in keywords:

            if keyword in line.lower():

                projects.append(line)

                break

    return list(dict.fromkeys(projects))


def extract_experience(text):

    keywords = [
        "experience",
        "intern",
        "internship",
        "worked",
        "developer",
        "engineer",
        "employment"
    ]

    experience = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        for keyword in keywords:

            if keyword in line.lower():

                experience.append(line)

                break

    return list(dict.fromkeys(experience))