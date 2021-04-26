from django import forms
from .models import Post,Comments

class PForms(forms.ModelForm):
	
	bodyofpost=forms.CharField(
		label='',
		widget=forms.Textarea(attrs={
			'rows':'5',
			'placeholder':'Say something....'
			}))

	image=forms.ImageField(label='Post Image From Here',required=False)


	class Meta:
		model=Post
		fields=['bodyofpost','image']


class CommentsForms(forms.ModelForm):
	
	comment=forms.CharField(
		label='',
		widget=forms.Textarea(attrs={
			'rows':'3',
			'placeholder':'Say something....'
			}))
	class Meta:
		model=Comments
		fields=['comment']
		