SKILLS = [
    "python",
    "django",
    "react",
    "javascript",
    "html",
    "css",
    "sql",
    "mysql",
    "postgresql",
    "java",
    "c++",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "ai"
]

def extract_skills(text):
    text = text.lower()

    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return found