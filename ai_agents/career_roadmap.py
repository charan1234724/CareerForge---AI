ROADMAPS = {

    "AI Engineer": [

        {
            "month": 1,
            "title": "Python Programming",
            "tasks": [
                "Master Python",
                "Object Oriented Programming",
                "Practice 50 coding problems"
            ]
        },

        {
            "month": 2,
            "title": "Machine Learning",
            "tasks": [
                "Learn NumPy",
                "Pandas",
                "Scikit-Learn"
            ]
        },

        {
            "month": 3,
            "title": "Deep Learning",
            "tasks": [
                "TensorFlow",
                "PyTorch",
                "CNN",
                "RNN"
            ]
        },

        {
            "month": 4,
            "title": "Generative AI",
            "tasks": [
                "Prompt Engineering",
                "LLMs",
                "LangChain",
                "RAG"
            ]
        },

        {
            "month": 5,
            "title": "Portfolio",
            "tasks": [
                "Build 3 AI Projects",
                "Deploy on GitHub"
            ]
        },

        {
            "month": 6,
            "title": "Placement Preparation",
            "tasks": [
                "DSA",
                "Interview Questions",
                "Resume Optimization"
            ]
        }

    ],

    "Frontend Developer": [

        {
            "month": 1,
            "title": "HTML & CSS",
            "tasks": [
                "Responsive Design",
                "Bootstrap",
                "Flexbox"
            ]
        },

        {
            "month": 2,
            "title": "JavaScript",
            "tasks": [
                "DOM",
                "ES6",
                "Fetch API"
            ]
        },

        {
            "month": 3,
            "title": "React",
            "tasks": [
                "Hooks",
                "Components",
                "Routing"
            ]
        },

        {
            "month": 4,
            "title": "Projects",
            "tasks": [
                "Portfolio Website",
                "Todo App",
                "Dashboard"
            ]
        },

        {
            "month": 5,
            "title": "Interview",
            "tasks": [
                "Frontend Interview",
                "React Questions"
            ]
        }

    ],

    "Full Stack Developer": [

        {
            "month": 1,
            "title": "Python & Django",
            "tasks": [
                "Python",
                "Django Basics"
            ]
        },

        {
            "month": 2,
            "title": "Database",
            "tasks": [
                "MySQL",
                "PostgreSQL"
            ]
        },

        {
            "month": 3,
            "title": "REST API",
            "tasks": [
                "Django REST Framework",
                "Authentication"
            ]
        },

        {
            "month": 4,
            "title": "Deployment",
            "tasks": [
                "Docker",
                "AWS",
                "GitHub Actions"
            ]
        },

        {
            "month": 5,
            "title": "Projects",
            "tasks": [
                "Job Portal",
                "E-commerce",
                "Chat Application"
            ]
        },

        {
            "month": 6,
            "title": "Interview",
            "tasks": [
                "System Design",
                "Coding Round"
            ]
        }

    ]

}


def generate_roadmap(career):

    return ROADMAPS.get(career, [])