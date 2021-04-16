from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display =['title','slug','pub_date']
class UserAdmin(admin.ModelAdmin):
    list_display =['name','course','userid','password','team']
class bWeekAdmin(admin.ModelAdmin):
    list_display =['week','num','sco','stu']


admin.site.register(Post,PostAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(biweekly,bWeekAdmin)
admin.site.register(Team)
admin.site.register(Week)
admin.site.register(Teacher)
admin.site.register(chatmes)

admin.site.register(kagglefile)
admin.site.register(kagscore)
admin.site.register(kagscore1)
admin.site.register(kagscore2)
admin.site.register(kagscore3)
admin.site.register(kagscore4)
