from django.shortcuts import render,redirect 
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.
def index(request):
    """Домашняя страница приложения learning_log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Выводии список тем."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)
@login_required
def topic(request, topic_id):
    """Выводит одну тему и все её записи"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)
@login_required
def new_topic(request):
    """Определяет новую тему"""
    if request.method != 'POST':
        """Данные не отправились : создается пустая форма"""
        form = TopicForm()
    else:
        """Отправленные данные POST: обработать данные"""
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    #Вывести пустую или недействительную форму
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html', context)
@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    # Получаем тему по её ID
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # Данные не отправлены; создаётся пустая форма
        form = EntryForm()
    else:
        # Обрабатываем отправленные данные POST
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # Создаём объект записи, но пока не сохраняем в базу
            new_entry = form.save(commit=False)
            # Привязываем запись к конкретной теме
            new_entry.topic = topic
            # Сохраняем запись в базе
            new_entry.save()
            # Перенаправляем пользователя на страницу темы
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    # Если форма пустая или недействительная, отобразить её снова
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую записью"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        #Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)


