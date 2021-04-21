from .models import Team


t=Team.objects.all()
t.update(test_t1=3)
t.update(test_t2=3)
t.update(test_t3=3)
t.update(test_t4=3)