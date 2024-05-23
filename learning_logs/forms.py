from django import forms
from .models import Topic, Entry, Rule

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class RuleForm(forms.ModelForm):

    class Meta:
        
        model = Rule
        fields = ['rule', 'ban']

class EntryForm(forms.ModelForm):

    class Meta:
    
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}