from django.shortcuts import render, redirect
from django.utils import timezone


tasks = [
    {
        'id': 1,
        'text': 'Faire les courses',
        'completed': False,
        'date': timezone.now().strftime('%a %d %b')
    },
    {
        'id': 2,
        'text': 'Préparer le rapport',
        'completed': True,
        'date': timezone.now().strftime('%a %d %b')
    }
]

def home(request):
    filter_type = request.GET.get('filter', 'all')
    search_term = request.GET.get('search', '').lower()
    
    
    filtered_tasks = tasks
    if filter_type == 'active':
        filtered_tasks = [t for t in tasks if not t['completed']]
    elif filter_type == 'completed':
        filtered_tasks = [t for t in tasks if t['completed']]
    
    
    if search_term:
        filtered_tasks = [t for t in filtered_tasks if search_term in t['text'].lower()]
    
    
    total_tasks = len(filtered_tasks)
    completed_tasks = len([t for t in filtered_tasks if t['completed']])
    
    context = {
        'tasks': filtered_tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'current_filter': filter_type,
        'search_term': search_term,
    }
    
    return render(request, 'home.html', context)

def add_task(request):
    global tasks
    if request.method == 'POST':
        task_text = request.POST.get('task_text', '').strip()
        if task_text:
            
            task_text = task_text[0].upper() + task_text[1:]
            
            new_task = {
                'id': max([t['id'] for t in tasks], default=0) + 1,
                'text': task_text,
                'completed': False,
                'date': timezone.now().strftime('%a %d %b')
            }
            tasks.append(new_task)
    
    return redirect('home')

def toggle_task(request, task_id):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    
    return redirect('home')

def delete_task(request, task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect('home')

def clear_completed(request):
    global tasks
    tasks = [t for t in tasks if not t['completed']]
    return redirect('home')