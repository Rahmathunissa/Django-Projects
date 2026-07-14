from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import SignUpForm, TaskForm
from .models import Task


class OwnerRequiredMixin(UserPassesTestMixin):
    """Stops user A from viewing/editing user B's task by guessing a URL."""
    def test_func(self):
        return self.get_object().owner == self.request.user


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user)
        status = self.request.GET.get('status')
        if status == 'completed':
            qs = qs.filter(completed=True)
        elif status == 'pending':
            qs = qs.filter(completed=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status'] = self.request.GET.get('status', 'all')
        return ctx


class TaskDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Task created.')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task-list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})