from django.urls import path
from . import views
from .views import ProblemsView, ProblemDetailView, CreateProblemView, ProblemDetailView, SubmitSolutionView, SolutionView, CompareSolutionsView
# SolutionDetailView

urlpatterns = [
    path('', views.home, name='compare-home'),
    path('about/', views.about, name='compare-about'),
    path('code/', views.code, name='compare-code'),
    path('datasets/', views.datasets, name='compare-datasets'),
    path('information/', views.information, name='compare-information'),
    path('myaccount/', views.myaccount, name='compare-myaccount'),
    path('solutions/',views.solutions,name='compare-solutions'),
    path('myproblems/',views.problems,name="compare-problems"),
    path('favourite/',views.favourite,name='compare-favourite'),
    path('problems/', ProblemsView.as_view(), name='problems'),
    path('problems/new/', CreateProblemView.as_view(), name='new_problem'),
    path('problems/<int:pk>/', ProblemDetailView.as_view(), name='problem_detail'),
    path('problems/<int:pk>/submit_solution/', SubmitSolutionView.as_view(), name='submit_solution'),
    path('hostpage/', views.hostpage, name='hostpage'),
    path('acceptDecline/', views.acceptDecline, name='acceptDecline'),
    path('hostProblems/', views.hostProblems, name='hostProblems'),
    path('accepted/', views.accepted, name='accepted'),
    path('rejected/', views.rejected, name='rejected'),
    path('userProblemStatus/', views.userProblemStatus, name='userProblemStatus'),
    path('problems/<int:pk>/solution_list/', SolutionView.as_view(), name='solution_list'),
    path('problems/<int:pk>/compare_solutions/', CompareSolutionsView.as_view(), name='compare_solutions'),
    # path('problems/<int:pk>/solution_list/<int:pk1>/', SolutionDetailView.as_view(), name='solution'),

]
