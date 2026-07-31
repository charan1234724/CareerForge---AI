from dataclasses import dataclass
import re


@dataclass
class ResumeData:

    name: str

    email: str

    phone: str

    github: str

    linkedin: str

    portfolio: str

    skills: list

    education: list

    experience: list

    projects: list

    certifications: list

    languages: list

    sections: dict


SECTION_HEADERS = {

    "skills":[
        "skills",
        "technical skills"
    ],

    "education":[
        "education",
        "academic"
    ],

    "experience":[
        "experience",
        "work experience",
        "internship"
    ],

    "projects":[
        "projects"
    ],

    "certifications":[
        "certifications",
        "certificate"
    ]
}


def split_sections(text):

    sections = {}

    current = "general"

    sections[current] = []

    for line in text.splitlines():

        line = line.strip()

        if not line:

            continue

        found = False

        lower = line.lower()

        for section, headers in SECTION_HEADERS.items():

            if lower in headers:

                current = section

                sections[current] = []

                found = True

                break

        if not found:

            sections[current].append(line)

    return sections


def extract_resume_data(resume):

    text = resume.resume_text or ""

    sections = split_sections(text)

    email = ""

    phone = ""

    github = ""

    linkedin = ""

    portfolio = ""

    email_match = re.findall(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    if email_match:

        email = email_match[0]

    phone_match = re.findall(
        r'\+?\d[\d\s-]{8,15}',
        text
    )

    if phone_match:

        phone = phone_match[0]

    github_match = re.search(
        r'github\.com/\S+',
        text,
        re.I
    )

    if github_match:

        github = github_match.group()

    linkedin_match = re.search(
        r'linkedin\.com/\S+',
        text,
        re.I
    )

    if linkedin_match:

        linkedin = linkedin_match.group()

    url_match = re.findall(
        r'https?://\S+',
        text
    )

    if url_match:

        portfolio = url_match[0]

    return ResumeData(

        name=resume.name,

        email=email,

        phone=phone,

        github=github,

        linkedin=linkedin,

        portfolio=portfolio,

        skills=sections.get("skills", []),

        education=sections.get("education", []),

        experience=sections.get("experience", []),

        projects=sections.get("projects", []),

        certifications=sections.get("certifications", []),

        languages=[],

        sections=sections

    )