from django.views.generic import FormView
from django import forms
from sandbox.example import models


class TestForm(forms.ModelForm):
    class Meta:
        model = models.Page
        exclude = []


class TestFromView(FormView):
    form_class = TestForm
    template_name = 'test_form.html'

