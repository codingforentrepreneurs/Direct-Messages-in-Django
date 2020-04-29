from django import forms

class ChannelMessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))