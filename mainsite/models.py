from django.db import models
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=200)
    slug=models.CharField(max_length=200)
    body=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-pub_date']

    def __uncode__(self):
        return self.title

class Team(models.Model):
    name=models.CharField(max_length=20,null=False)

    class Meta:
        ordering = ['name']

    def __uncode__(self):
        return self.name
    def __str__(self):
        return self.name

class User(models.Model):
    name=models.CharField(max_length=20,null=False)
    class_choices=[
        ('py','Python程式設計'),
        ('ml','機器學習'),
    ]
    course=models.CharField(max_length=2,choices=class_choices)
    password=models.CharField(max_length=20,null=False,default='0000')
    userid=models.CharField(max_length=9,null=True)
    team=models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True)
    

    class Meta:
        ordering = ['userid']

    def __uncode__(self):
        return self.userid
    def __str__(self):
        return self.name
class Week(models.Model):
    name=models.CharField(max_length=20 ,unique=True)
    
    def __uncode__(self):
        return self.name
    def __str__(self):
        return self.name

class biweekly(models.Model):
    week=models.ForeignKey(Week,on_delete=models.CASCADE)
    num1=models.FloatField(null=True,default=0.0)
    num2=models.FloatField(null=True,default=0.0)
    num3=models.FloatField(null=True,default=0.0)
    num4=models.FloatField(null=True,default=0.0)
    stu=models.ForeignKey(User,on_delete=models.CASCADE)


    def __uncode__(self):
        return self.week.name
    def __str__(self):
        return self.week.name

class Teacher(models.Model):
    psw=models.CharField(max_length=20,null=False,default='0000')
    def __uncode__(self):
        return self.psw
    def __str__(self):
        return self.psw