from django.contrib import admin
from .models import Problem, Dataset, Solution

admin.site.register(Problem)
admin.site.register(Dataset)
admin.site.register(Solution)