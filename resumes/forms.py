from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):

    class Meta:

        model = Resume

        fields = [

            "name",

            "pdf"

        ]

    def __init__(

        self,

        *args,

        **kwargs

    ):

        super().__init__(

            *args,

            **kwargs

        )

        for field in self.fields.values():

            field.widget.attrs.update(

                {

                    "class":"form-control"

                }

            )