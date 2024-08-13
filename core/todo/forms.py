from django import forms


class TaskForm(forms.Form):
    task = forms.CharField(widget=forms.TextInput)
