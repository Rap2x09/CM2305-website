import pymysql
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from utils import sqlhelper
from .models import Problem, Dataset, Solution
from .forms import SubmitProbSpecForm
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.forms.models import inlineformset_factory
from django.forms import Textarea, FileInput
from .validators import validate_file
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404

def home(request):
    context = {
        'posts': Problem.objects.filter(status='Accept')
    }
    return render(request, 'compare/home.html', context)

class ProblemsView(ListView):
    template_name = 'compare/problems.html'
    model = Problem
    context_object_name = 'problemsList'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['problemsList'] = Problem.objects.all()
    #     context['solutionList'] = Solution.objects.all()

    #     return context

    # def get_queryset(self):
    #     return Problem.objects.order_by('problemID')

class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'compare/problem_detail.html'

class SolutionDetailView(DetailView):
    model = Solution
    template_name = 'compare/solution.html'

    # def get_context_data(self, **kwargs):
    #     context = super(SolutionDetailView, self).get_context_data(**kwargs)
    #     solution = Solution.objects.get(id=self.kwargs.get('pk1', ''))
    #     context['solution'] = solution
    #     return context

    # def get_success_url(self):
    #     return reverse('solution', kwargs={'pk1': self.object.pk})


childFormset = inlineformset_factory(Problem, Dataset, fields=('dataset', 'datasetDesc',), can_delete=False, extra=1, 
    widgets={'datasetDesc': Textarea(attrs={'required': True}),'dataset': FileInput(attrs={'required': True, 'validators' : validate_file})})

class CreateProblemView(LoginRequiredMixin, CreateView):
    model = Problem
    template_name = 'compare/new_problem.html'
    fields = ['title', 'problemInfo', 'evaluationCode',]
    login_url = 'login'


    def get_context_data(self, **kwargs):
        data = super(CreateProblemView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['datasets'] = childFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['datasets'] = childFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        datasets = context["datasets"]
        form.instance.localUser = self.request.user
        self.object = form.save()
        if datasets.is_valid():
            datasets.instance = self.object
            datasets.save()
        return super(CreateProblemView, self).form_valid(form)

    def get_success_url(self):
        return reverse('problem_detail', kwargs={'pk': self.object.pk})

class SubmitSolutionView(LoginRequiredMixin, CreateView):
    model = Solution
    template_name = 'compare/submit_solution.html'
    fields = ['solutionCode']
    login_url = 'login'

    def get_success_url(self):
        problemID = self.kwargs['pk']
        return reverse_lazy('problem_detail', kwargs={'pk': problemID})

    def form_valid(self, form):
        problem = get_object_or_404(Problem, pk=self.kwargs['pk'])
        form.instance.problem = problem
        form.instance.localUser = self.request.user
        return super(SubmitSolutionView, self).form_valid(form)

class SolutionView(LoginRequiredMixin, ListView):
    template_name = 'compare/solution_list.html'
    context_object_name = 'solutionList'
    # queryset = 

    def get_queryset(self):
        problemID = self.kwargs['pk']
        # self.problemID = get_object_or_404(Problem, )
        return Solution.objects.filter(problem_id = problemID)

    # def get_success_url(self):
    #     problemID = self.kwargs['pk']
    #     return reverse('solution_list', kwargs={'pk': problemID})
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

class CompareSolutionsView(LoginRequiredMixin, ListView):
    template_name = 'compare/compare_solutions.html'
    context_object_name = 'solutionList'
    # queryset = 

    def get_queryset(self):
        problemID = self.kwargs['pk']
        # self.problemID = get_object_or_404(Problem, )
        return Solution.objects.filter(problem_id = problemID)

def code(request):
    return render(request, 'compare/code.html', {'title': 'Code'})


def about(request):
    form = SubmitProbSpecForm()
    return render(request, 'compare/about.html', {'form': form})


def datasets(request):
    context = {
        'datasets': Dataset.objects.all()
    }
    return render(request, 'compare/datasets.html', context)


def information(request):
    return render(request, 'compare/information.html', {'title': 'Dataset Information'})


def myaccount(request):
    if request.user.is_authenticated:
        nid = request.user.id
        username = sqlhelper.get_one("select username from auth_user where id=%s", [nid])
        email = sqlhelper.get_one("select email from auth_user where id=%s", [nid])
        print(username)
        if request.method == 'POST':
            nid = request.POST.get('id')
            opw = request.POST.get('Opwd')
            npw = request.POST.get('Npwd')
            cpw = request.POST.get('Cpwd')
            if not request.user.check_password(opw):
                error = "Original Password is Wrong"
                return render(request, 'compare/myaccount.html', {'id': nid, 'username': username, 'email': email, 'error': error})
            if npw != cpw:
                error = "Inconsistent new password entry"
                return render(request, 'compare/myaccount.html', {'id': nid, 'username': username, 'email': email, 'error': error})
            request.user.set_password(npw)
            request.user.save()
            logout(request)
            return render(request, 'compare/home.html')
        return render(request, 'compare/myaccount.html', {'id': nid, 'username': username, 'email': email})
    else:
        return redirect('login')


def solutions(request):
    if request.user.is_authenticated:
        nid = request.user.id
        try:
            solution_list = Solution.objects.filter(localUser=nid).all().values_list("problem__title")
        except Solution.DoesNotExist:
            solution_list = None
        return render(request, 'compare/solutions.html', {'solution_list': solution_list})
    else:
        return redirect('login')


def problems(request):
    if request.user.is_authenticated:
        nid = request.user.id
        try:
            problem_list = Problem.objects.filter(localUser=nid)
        except Problem.DoesNotExist:
            problem_list = None
        return render(request, 'compare/myproblem.html', {'problem_list': problem_list})
    else:
        return redirect('login')


def favourite(request):
    # When having DB, get the userid for post all the information between webpage
    # This sql statement need to be rewrite
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123123', db='mydb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id, solution from solutions")
    favourite_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'compare/favourite.html', {'favourite_list': favourite_list})


def hostpage(request):
    if request.user.is_superuser:
        return render(request, 'compare/hostpage.html', {'title': 'Host'})
    else:
        return render(request, 'compare/mustbehost.html', {'title': 'Must Be Host'})


def acceptDecline(request):
    if request.user.is_superuser:
        context = {
        'posts': Problem.objects.all()
        }
        if request.method == 'POST':
            post = Problem.objects.get(problemID=request.POST.get('id'))

            if request.POST.get('status'):
                post.status = request.POST.get('status')
                post.save()
        return render(request, 'compare/acceptDecline.html', context, {'title': 'Accept/Reject Problem Specification'})
   
    else:
        return render(request, 'compare/mustbehost.html', {'title': 'Must Be Host'})

def accepted(request):
    if request.user.is_superuser:
        context = {
        'posts': Problem.objects.filter(status='Accept')
        }
        return render(request, 'compare/accepted.html', context, {'title': 'Accepted Problems'})
    else:
        return render(request, 'compare/mustbehost.html', {'title': 'Must Be Host'})


def rejected(request):
    if request.user.is_superuser:
        context = {
        'posts': Problem.objects.filter(status='Reject')
        }
        return render(request, 'compare/rejected.html', context, {'title': 'Rejected Problems'})
    else:
        return render(request, 'compare/mustbehost.html', {'title': 'Must Be Host'})



def hostProblems(request):
    if request.user.is_superuser:
        context = {
        'posts': Problem.objects.filter(status='Accept')
        }
        return render(request, 'compare/hostProblems.html', context, {'title': 'My Hosted Problems'})
    else:
        return render(request, 'compare/mustbehost.html', {'title': 'Must Be Host'})



def userProblemStatus(request):
    if request.user.is_authenticated:
        nid = request.user.id
        try:
            problem_list = Problem.objects.filter(localUser=nid)
        except Problem.DoesNotExist:
            problem_list = None
        return render(request, 'compare/userProblemStatus.html', {'problem_list': problem_list})
    else:
        return redirect('login')
