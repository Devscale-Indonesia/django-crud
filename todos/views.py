from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Todo
from django.views import View
from django.contrib import messages

class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        todos = Todo.objects.filter(actor=request.user)
        return render(request, 'index.html', {'todos': todos})

    def post(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title and not content:
            messages.error(request, "Title and Content are required")

        else:
            Todo.objects.create(title=title, content=content, actor=request.user)

        return redirect('index')


class DetailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        todo = Todo.objects.get(id=id)

        return render(request, 'detail.html', {'todo': todo})


class DeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, id):
        todo = Todo.objects.get(id=id)
        todo.delete()

        return redirect('index')


class UpdateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id):
        todo = Todo.objects.get(id=id)

        return render(request, 'edit.html', { 'todo': todo })

    def post(self, request, id):
        title = request.POST.get('title')
        content = request.POST.get('content')

        todo = Todo.objects.get(id=id)

        todo.title = title
        todo.content = content
        todo.save()

        return redirect('index')