from django.utils import timezone
import pytz

from .models import StudentProfile


def current_time(request):

    if request.user.is_authenticated:

        try:
            profile = StudentProfile.objects.get(user=request.user)

            tz = pytz.timezone(profile.timezone)

            current = timezone.now().astimezone(tz)

            current = current.strftime("%d %b %Y, %I:%M %p")

        except Exception:

            current = timezone.now().strftime("%d %b %Y, %I:%M %p")

    else:

        current = timezone.now().strftime("%d %b %Y, %I:%M %p")

    return {
        "current_time": current
    }

def language_labels(request):

    if request.user.is_authenticated:

        try:

            profile = StudentProfile.objects.get(
                user=request.user
            )

            language = profile.language

        except:

            language = "English"

    else:

        language = "English"

    if language == "te":

        labels = {

    "dashboard": "డాష్‌బోర్డ్",

    "profile": "ప్రొఫైల్",

    "settings": "సెట్టింగ్స్",

    "logout": "లాగ్ అవుట్",

    "welcome": "స్వాగతం",

    "upload_resume": "రెజ్యూమ్ అప్లోడ్",

    "resume_summary": "రెజ్యూమ్ సారాంశం",

    "resume_improvement": "రెజ్యూమ్ మెరుగుదల",

    "career_copilot": "కెరీర్ కోపైలట్",

    "career_roadmap": "కెరీర్ రోడ్‌మ్యాప్",

    "placement_prediction": "ప్లేస్‌మెంట్ అంచనా",

    "interview_prep": "ఇంటర్వ్యూ సిద్ధత",

    "mock_interview": "మాక్ ఇంటర్వ్యూ",

    "real_jobs": "నిజమైన ఉద్యోగాలు",

    "saved_jobs": "సేవ్ చేసిన ఉద్యోగాలు",

    "applications": "దరఖాస్తులు",

    "notifications": "నోటిఫికేషన్లు",

    "analytics": "విశ్లేషణలు",

}

    elif language == "hi":

        labels = {

    "dashboard": "डैशबोर्ड",

    "profile": "प्रोफ़ाइल",

    "settings": "सेटिंग्स",

    "logout": "लॉग आउट",

    "welcome": "स्वागत है",

    "upload_resume": "रिज़्यूमे अपलोड",

    "resume_summary": "रिज़्यूमे सारांश",

    "resume_improvement": "रिज़्यूमे सुधार",

    "career_copilot": "करियर कोपायलट",

    "career_roadmap": "करियर रोडमैप",

    "placement_prediction": "प्लेसमेंट भविष्यवाणी",

    "interview_prep": "इंटरव्यू तैयारी",

    "mock_interview": "मॉक इंटरव्यू",

    "real_jobs": "वास्तविक नौकरियां",

    "saved_jobs": "सहेजी गई नौकरियां",

    "applications": "आवेदन",

    "notifications": "सूचनाएं",

    "analytics": "विश्लेषण",

}

    else:

        labels = {

    "dashboard": "Dashboard",

    "profile": "Profile",

    "settings": "Settings",

    "logout": "Logout",

    "welcome": "Welcome",

    "upload_resume": "Upload Resume",

    "resume_summary": "Resume Summary",

    "resume_improvement": "Resume Improvement",

    "career_copilot": "Career Copilot",

    "career_roadmap": "Career Roadmap",

    "placement_prediction": "Placement Prediction",

    "interview_prep": "Interview Prep",

    "mock_interview": "Mock Interview",

    "real_jobs": "Real Jobs",

    "saved_jobs": "Saved Jobs",

    "applications": "Applications",

    "notifications": "Notifications",

    "analytics": "Analytics",

}

    return {

        "labels": labels

    }