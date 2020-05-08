from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from .validators import validate_file
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver
from django.forms.models import inlineformset_factory


class Problem(models.Model):
    problemID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name= 'Title')
    problemInfo = models.TextField(verbose_name= 'Problem Details') # max_length=4000
    evaluationCode = models.TextField(verbose_name='Evaluation Code')
    isValid = models.BooleanField(default=False, verbose_name= 'Valid?')
    isReleased = models.BooleanField(default=False, verbose_name= 'Released?')
    localUser = models.ForeignKey(User, on_delete=models.CASCADE, default="", editable=False)
    status = models.CharField(max_length=30, default="Pending")
    dateSubmitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"'{self.title}', '{self.problemInfo}', '{self.evaluationCode}', '{self.isValid}', '{self.isReleased}')"

    # def get_absolute_url(self):
    #     return reverse('problem_detail', kwargs={'pk': self.pk})
class Dataset(models.Model):
    dataID = models.AutoField(primary_key=True)
    dataset = models.FileField(upload_to='datasets/', validators=[validate_file])
    datasetDesc = models.CharField(max_length=100, verbose_name= 'Dataset Short Description')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return f"'{self.dataset}', '{self.datasetDesc}'"

    def filename(self):
        return os.path.basename(self.dataset.name)

class Solution(models.Model):
    solutionID = models.AutoField(primary_key=True)
    solutionCode = models.TextField(verbose_name='Solution')
    isVerified = models.BooleanField(default=False)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    localUser = models.ForeignKey(User, on_delete=models.CASCADE, default="", editable=False)
    dateSubmitted = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"'{self.solutionCode}', '{self.isVerified}'"

@receiver(post_delete, sender=Dataset)
def file_delete_handler(sender, **kwargs):
    file = kwargs['instance']
    storage, path = file.dataset.storage, file.dataset.path
    storage.delete(path)



# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title


# class Datasets(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.CharField(max_length=100)

#     def __str__(self):
#         return self.title
