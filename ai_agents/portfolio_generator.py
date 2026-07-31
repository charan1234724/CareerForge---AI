from ai_agents.llm_service import ask_llm


def generate_portfolio(resume_text):

    prompt = f"""
You are a senior UI/UX designer and professional portfolio developer.

Generate a COMPLETE modern personal portfolio website using HTML5 and Bootstrap 5 only.

Resume:

{resume_text}

Requirements:

Design Style:
- Modern SaaS UI
- Glassmorphism
- Gradient Hero Section
- Professional Blue Theme
- Responsive Layout
- Beautiful Cards
- Rounded Corners
- Hover Animations
- Font Awesome Icons
- Smooth Scroll
- Attractive Buttons
- Professional Footer

Include these sections:

1. Hero Section
- Full Name
- Professional Title
- Short Introduction
- Resume Button
- Contact Button

2. About Me

3. Technical Skills
Display skills as beautiful badges.

4. Featured Projects
Use modern project cards.

Each project should contain:
- Title
- Description
- Technologies
- GitHub Button
- Live Demo Button

5. Education Timeline

6. Internship / Experience Timeline

7. Certifications

8. Achievements

9. Contact Section

Include:
- Email
- Phone
- LinkedIn
- GitHub

10. Professional Footer

Extra Features:

- Animated Progress Bars
- Skills Cards
- Project Cards
- Timeline Design
- Statistics Section
- Scroll Animations
- Bootstrap Icons
- Mobile Responsive

Rules:

Return ONLY complete HTML.

Do NOT use Markdown.

Do NOT explain anything.

Return a complete webpage.
"""

    return ask_llm(prompt)