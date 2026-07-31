from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

import re
from .models import SupportTicket
from .models import BugReport
class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:

        model = User

        fields = [

            "username",

            "email",

            "password1",

            "password2"

        ]

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field in self.fields.values():

            field.widget.attrs.update({

                "class":"form-control"

            })
        self.fields["password1"].widget.attrs.update({
    "class": "form-control",
    "placeholder": "New Password"
})

        self.fields["password2"].widget.attrs.update({
    "class": "form-control",
    "placeholder": "Confirm Password"
})

    def clean_email(self):

        email=self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():

            raise ValidationError(

                "This email is already registered."

            )

        return email

    def clean_password1(self):

        password=self.cleaned_data.get("password1")

        if len(password)<8:

            raise ValidationError(

                "Password must contain at least 8 characters."

            )

        if not re.search(r"[A-Z]",password):

            raise ValidationError(

                "Password must contain one uppercase letter."

            )

        if not re.search(r"[a-z]",password):

            raise ValidationError(

                "Password must contain one lowercase letter."

            )

        if not re.search(r"\d",password):

            raise ValidationError(

                "Password must contain one number."

            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",password):

            raise ValidationError(

                "Password must contain one special character."

            )

        return password
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms


class CustomPasswordResetForm(PasswordResetForm):

    def clean_email(self):

        email = self.cleaned_data["email"]

        if not User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                "❌ No account found with this email address."
            )

        return email
from django import forms

from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):

    class Meta:

        model = StudentProfile

        exclude = ["user"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if isinstance(field.widget, forms.Select):

                field.widget.attrs.update({

                "class": "form-select"

            })

            elif isinstance(field.widget, forms.CheckboxInput):

                field.widget.attrs.update({

                "class": "form-check-input"

            })

            else:

                field.widget.attrs.update({

                "class": "form-control",

                "placeholder": field.label,

            })

        self.fields["bio"].widget.attrs.update({

        "rows": 4

    })
        # -------------------------
        # Notification IDs
        # -------------------------

        self.fields["email_notifications"].widget.attrs.update({

    "id": "email_notifications",

    "class": "form-check-input notification-toggle"

})

        self.fields["job_alerts"].widget.attrs.update({

    "id": "job_alerts",

    "class": "form-check-input notification-toggle"

})

        self.fields["interview_reminders"].widget.attrs.update({

    "id": "interview_reminders",

    "class": "form-check-input notification-toggle"

})

        self.fields["weekly_report"].widget.attrs.update({

    "id": "weekly_report",

    "class": "form-check-input notification-toggle"

})
  
class SupportTicketForm(forms.ModelForm):

    class Meta:

        model = SupportTicket

        fields = [

            "subject",

            "message"

        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({

            "class": "form-control",

            "placeholder": "Subject"

        })

        self.fields["message"].widget.attrs.update({

            "class": "form-control",

            "rows": 6,

            "placeholder": "Describe your issue..."

        })

class BugReportForm(forms.ModelForm):

    class Meta:

        model = BugReport

        fields = [

            "title",

            "description",

            "page",

            "screenshot"

        ]

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"

        self.fields["description"].widget.attrs["rows"] = 6