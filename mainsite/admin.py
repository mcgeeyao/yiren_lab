from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display =['title','slug','pub_date']
class UserAdmin(admin.ModelAdmin):
    list_display =['name','course','userid','password','team']
class bWeekAdmin(admin.ModelAdmin):
    list_display =['week','num1','num2','num3','num4','stu']


admin.site.register(Post,PostAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(biweekly,bWeekAdmin)
admin.site.register(Team)
admin.site.register(Week)
admin.site.register(Teacher)