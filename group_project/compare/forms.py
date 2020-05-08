from django import forms

class SubmitProbSpecForm(forms.Form):
	title = forms.CharField(label="Title of Problem Specification")
	description = forms.CharField(widget=forms.Textarea, label="Description: ")
	paste_code = forms.CharField(widget=forms.Textarea, label="Please enter your code here: ")
