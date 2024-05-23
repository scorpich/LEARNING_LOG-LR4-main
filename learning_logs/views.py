from django.shortcuts import render, redirect
from .models import Topic, Entry, Rule
from .forms import TopicForm, EntryForm, RuleForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
     return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
     if request.user.is_superuser:
         topics = Topic.objects.order_by('date_added')
     else:
         topics = Topic.objects.filter(owner=request.user).order_by('date_added')
     context = {'topics': topics}
     return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
     topic = Topic.objects.get(id=topic_id)
     if request.user.is_superuser == False:
        if topic.owner != request.user:
           raise Http404
     entries = topic.entry_set.order_by('-date_added')
     context = {'topic': topic, 'entries': entries}
     return render(request, 'learning_logs/topic.html', context)

@login_required
def rules(request):
    rules = Rule.objects.all()
    return render(request, 'learning_logs/rules.html', {'rules': rules})

@login_required
def new_rule(request):
    form = RuleForm(data=request.POST)

    if request.method == 'POST':
        form = RuleForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:rules')
        
    context = {'form': form}
    return render(request, 'learning_logs/new_rule.html', context)

@login_required
def edit_rule(request, rule_id):
     rule = Rule.objects.get(id=rule_id)
     if request.method != 'POST':
          form = RuleForm(instance=rule)
     else: 
          form = RuleForm(instance=rule, data=request.POST)
          if form.is_valid():
             form.save()
             return redirect('learning_logs:rules')
        
     context = {'rule' : rule, 'form': form}
     return render(request, 'learning_logs/edit_rule.html', context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
     topic = Topic.objects.get(id=topic_id)
     if request.method != 'POST':
          form = EntryForm()
     else:
          form = EntryForm(data=request.POST)
          if form.is_valid():
               new_entry = form.save(commit=False)
               new_entry.topic = topic
               new_entry.save()
               return redirect('learning_logs:topic', topic_id=topic_id)
     context = {'topic': topic, 'form': form}
     return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
     entry = Entry.objects.get(id=entry_id)
     topic = entry.topic
     if request.user.is_superuser == False:
        if topic.owner != request.user:
           raise Http404

     if request.method != 'POST':
          form = EntryForm(instance=entry)
     else:
          form = EntryForm(instance=entry, data=request.POST)
          if form.is_valid():
               form.save()
               return redirect('learning_logs:topic', topic_id=topic.id)
     context = {'entry': entry, 'topic': topic, 'form': form}
     return render(request, 'learning_logs/edit_entry.html', context)