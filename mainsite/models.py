from django.db import models
from django.utils import timezone

# Create your models here.
'''
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
    test_t=models.IntegerField(default=0,null=True)
    test_t1=models.IntegerField(default=0,null=True)
    test_t2=models.IntegerField(default=0,null=True)
    test_t3=models.IntegerField(default=0,null=True)
    test_t4=models.IntegerField(default=0,null=True)

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
    nums=models.IntegerField(null=True)

    def __uncode__(self):
        return self.name
    def __str__(self):
        return self.name

class biweekly(models.Model):
    week=models.ForeignKey(Week,on_delete=models.CASCADE)
    sco=models.FloatField(null=True,default=0.0)
    num=models.IntegerField(null=True)
    stu=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ['week','num']

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



class kagglefile(models.Model):
    kaggle_field = models.FileField(null=True)

class kagscore(models.Model):
    date=models.DateTimeField(auto_now=False, auto_now_add=False,default=timezone.now,null=True)
    sco=models.FloatField(null=True,default=0.0)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __uncode__(self):
        return self.team.name
    def __str__(self):
        return self.team.name

class kagscore1(models.Model):
    date=models.DateTimeField(auto_now=False, auto_now_add=False,default=timezone.now,null=True)
    sco=models.FloatField(null=True,default=0.0)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __uncode__(self):
        return self.team.name
    def __str__(self):
        return self.team.name

class kagscore2(models.Model):
    date=models.DateTimeField(auto_now=False, auto_now_add=False,default=timezone.now,null=True)
    sco=models.FloatField(null=True,default=0.0)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __uncode__(self):
        return self.team.name
    def __str__(self):
        return self.team.name

class kagscore3(models.Model):
    date=models.DateTimeField(auto_now=False, auto_now_add=False,default=timezone.now,null=True)
    sco=models.FloatField(null=True,default=0.0)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __uncode__(self):
        return self.team.name
    def __str__(self):
        return self.team.name

class kagscore4(models.Model):
    date=models.DateTimeField(auto_now=False, auto_now_add=False,default=timezone.now,null=True)
    sco=models.FloatField(null=True,default=0.0)
    team=models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']

    def __uncode__(self):
        return self.team.name
    def __str__(self):
        return self.team.name











class chatmes(models.Model):
    text=models.CharField(max_length=500,null=False)
    def __uncode__(self):
        return self.text
    def __str__(self):
        return self.text
'''