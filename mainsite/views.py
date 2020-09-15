
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.shortcuts import render,redirect
from django.http import HttpResponse ,Http404,JsonResponse
from django.db.models import Count
from datetime import datetime
from mainsite import forms
from .models import *

# Create your views here.
def index(request):
    posts=Post.objects.all()
    template=get_template('index.html')
    now=datetime.now()
    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    html=template.render(locals())
    return HttpResponse(html)

def login(request):
    if request.method=="POST":
        login_form=forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_id=request.POST["userid"].strip()
            login_password=request.POST["password"]
            try:
                user=User.objects.get(userid=login_id)
                if user.password==login_password:
                    response=redirect("/")
                    request.session['userid']=user.userid
                    request.session['course']=user.course
                    request.session['name']=user.name
                    return redirect("/")
                else:
                    message="學號或密碼錯誤"
            except:
                message='查無此學號'
        else:
            message="請檢查輸入的欄位"
    else:
        login_form=forms.LoginForm()
    #template=get_template("login.html")
    request_context=RequestContext(request)
    now=datetime.now()
    request_context.push(locals())
    #html=template.render(request_context)
    return TemplateResponse(request, 'login.html', locals())

def changepsw(request):
    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    else:
        redirect('/')
    if request.method=="POST":
        form=forms.changepsw(request.POST)
        if form.is_valid():
            opsw=request.POST["opsw"]
            npsw=request.POST["npsw"]
            npsw2=request.POST["npsw2"]
            #try:
            user=User.objects.filter(userid=userid)
            if user[0].password==opsw:
                if npsw==npsw2:
                    user.update(password=npsw)
                    return redirect("/userpro/")
                else:
                    message="兩次密碼不同"
            else:
                message="密碼錯誤"
            #except:
                #message='錯誤'
        else:
            message="請檢查輸入的欄位"
    else:
        form=forms.changepsw()
    now=datetime.now()
    return TemplateResponse(request, 'changepsw.html', locals())

def teachlog(request):
    if request.method=="POST":
        login_form=forms.teachlog(request.POST)
        if login_form.is_valid():
            login_password=request.POST["psw"]
            try:
                user=Teacher.objects.get(psw=login_password)
                request.session['psw']=login_password
                return redirect("/teacher/")
            except:
                message='密碼錯誤'
        else:
            message="請檢查輸入的欄位"
    else:
        login_form=forms.teachlog()
    return TemplateResponse(request, 'teachlog.html', locals())

def teachlogout(request):
    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    now=datetime.now()
    request.session.pop("psw",None)
    return TemplateResponse(request, 'index.html', locals())

def teacher(request):
    if 'psw' not in request.session:
        return redirect("/teachlog/")
    no=request.session['psw']
    now=datetime.now()
    teamsum=Team.objects.all().aggregate(Count('name'))["name__count"]                    #這是組數
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]                    #week數
    teams=Team.objects.all().order_by('id').values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    memid=[]
    members=[]
    tolsum=[]
    sesuser=[]
    for j in range(teamsum):
        memid.append([])
        members.append([])
        tolsum.append([])
        sesuser.append([])

    for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id']).values()
                memid[j].append(locteamuser[k]['userid'])
                members[j].append(locteamuser[k]['name'])                                             #這 members 做出來是(組數，組員name)
                tolsum[j].append(0)

    for i in range(weeksum):
        tol.append([])
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            tol[i].append([])
            for k in range(mem):
                tol[i][j].append([])

    for i in range(weeksum):
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id'],week=weeks[i]['id']).order_by('num').values()
                for s in range(weeknums[i]):
                    tol[i][j][k].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
                    tolsum[j][k]=tolsum[j][k]+score[s]['sco']

    table1=[]
    for j in range(len(members)):
        table1.append(f'''<tr>
                    <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                    <td>{memid[j][0]}</td>
                    <td>{members[j][0]}</td>
                    ''')
        for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][0][b]}</td>')
        table1.append(f'<td>{tolsum[j][0]}</td></tr>')
        for i in range(1,len(members[j])):
            table1.append(f'''<tr>
            <td>{memid[j][i]}</td>
            <td>{members[j][i]}</td>
            ''')
            for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][i][b]}</td>')
            table1.append(f'<td>{tolsum[j][i]}</td></tr>')
        
    table1=''.join(table1)
    weekna=[]
    weeks=Week.objects.all().order_by('id').values()
    for w in weeks:
        weekna.append((w['id'],w['name']))
    teamna=[]
    teams=Team.objects.all().order_by('id').values()
    for t in teams:
        teamna.append((t['id'],t['name']))
    '''if request.method=="POST":
        try:
            week=request.POST["week"]
            teamname=request.POST["teamname"]
            team=Team.objects.get(id=teamname).__dict__
            week=Week.objects.get(id=week).__dict__
            return redirect(f"/scoring/{team['name']}/{week['name']}")
        except:
            message='錯誤'
    else:
        pass'''
    if request.method=="POST":
        try:
            week=request.POST["week"]
            teamname=request.POST["teamname"]
            w=Week.objects.get(id=week).__dict__
            team=Team.objects.get(id=teamname).__dict__
            user=User.objects.filter(team=team['id']).order_by('id')
            userv=User.objects.filter(team=team['id']).order_by('id').values()
            for u in range(len(userv)):
                for n in range(w['nums']):
                    sco=request.POST["sco"+str(u)+str(n)]
                    b=biweekly.objects.filter(week=w['id'],stu=userv[u]['id'],num=n+1)
                    b.update(sco=sco)
            return redirect('/teacher/')
        except:
            message='發生錯誤'
    else:
        table=[]
        for we in range(len(weeks)):
            table.append([])
            for te in range(len(teams)):
                table[we].append([])
        for we in range(len(weeks)):
            for te in range(len(teams)):
                w=Week.objects.get(name=weeks[we]['name']).__dict__
                team=Team.objects.get(name=teams[te]['name']).__dict__
                user=User.objects.filter(team=team['id']).order_by('id')
                userv=User.objects.filter(team=team['id']).order_by('id').values()
                orig=[]
                
                for u in range(len(userv)):
                    orig.append([])
                    b=biweekly.objects.filter(week=w['id'],stu=userv[u]['id']).order_by('num').values()
                    for s in b:
                        orig[u].append(s['sco'])

                table[we][te].append('<tr><th></th>')
                for n in range(w['nums']):
                    table[we][te].append(f'<th>NO.{n+1}</th>')
                table[we][te].append('</tr>')
                for u in range(len(userv)):
                    table[we][te].append(f'''<tr><td>{userv[u]['name']}</td>''')
                    for n in range(w['nums']):
                        table[we][te].append(f'''<td><label for="{"sco"+str(u)+str(n)}"></label><input type="number" step="0.01" value="{orig[u][n]}" name={"sco"+str(u)+str(n)} id={"sco"+str(u)+str(n)}><br></td>''')
                    table[we][te].append('</tr>')
                table[we][te]=''.join(table[we][te])


    return TemplateResponse(request, 'teacher.html', locals())

def scoring(request,team=None,week=None):
    if 'psw' not in request.session:
        return redirect("/teachlog/")
    no=request.session['psw']
    now=datetime.now()
    teamsum=Team.objects.all().aggregate(Count('name'))["name__count"]                    #這是組數
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]                    #week數
    teams=Team.objects.all().order_by('id').values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    memid=[]
    members=[]
    tolsum=[]
    sesuser=[]
    for j in range(teamsum):
        memid.append([])
        members.append([])
        tolsum.append([])
        sesuser.append([])

    for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id']).values()
                memid[j].append(locteamuser[k]['userid'])
                members[j].append(locteamuser[k]['name'])                                             #這 members 做出來是(組數，組員name)
                tolsum[j].append(0)

    for i in range(weeksum):
        tol.append([])
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            tol[i].append([])
            for k in range(mem):
                tol[i][j].append([])

    for i in range(weeksum):
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id'],week=weeks[i]['id']).order_by('num').values()
                for s in range(weeknums[i]):
                    tol[i][j][k].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
                    tolsum[j][k]=tolsum[j][k]+score[s]['sco']

    table1=[]
    for j in range(len(members)):
        table1.append(f'''<tr>
                    <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                    <td>{memid[j][0]}</td>
                    <td>{members[j][0]}</td>
                    ''')
        for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][0][b]}</td>')
        table1.append(f'<td>{tolsum[j][0]}</td></tr>')
        for i in range(1,len(members[j])):
            table1.append(f'''<tr>
            <td>{memid[j][i]}</td>
            <td>{members[j][i]}</td>
            ''')
            for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][i][b]}</td>')
            table1.append(f'<td>{tolsum[j][i]}</td></tr>')
        
    table1=''.join(table1)
    if request.method=="POST":
        try:
            w=Week.objects.get(name=week).__dict__
            team=Team.objects.get(name=team).__dict__
            user=User.objects.filter(team=team['id']).order_by('id')
            userv=User.objects.filter(team=team['id']).order_by('id').values()
            for u in range(len(userv)):
                for n in range(w['nums']):
                    sco=request.POST["sco"+str(u)+str(n)]
                    b=biweekly.objects.filter(week=w['id'],stu=userv[u]['id'],num=n+1)
                    b.update(sco=sco)
            return redirect('/teacher/')
        except:
            message='錯誤,請確認是否輸入為空'
    else:
        w=Week.objects.get(name=week).__dict__
        team=Team.objects.get(name=team).__dict__
        user=User.objects.filter(team=team['id']).order_by('id')
        userv=User.objects.filter(team=team['id']).order_by('id').values()
        orig=[]
        
        for u in range(len(userv)):
            orig.append([])
            b=biweekly.objects.filter(week=w['id'],stu=userv[u]['id']).order_by('num').values()
            for s in b:
                orig[u].append(s['sco'])

        table=[]
        table.append('<tr><th></th>')
        for n in range(w['nums']):
            table.append(f'<th>NO.{n+1}</th>')
        table.append('</tr>')
        for u in range(len(userv)):
            table.append(f'''<tr><td>{userv[u]['name']}</td>''')
            for n in range(w['nums']):
                table.append(f'''<td><label for="{"sco"+str(u)+str(n)}"></label><input type="number" step="0.01" value="{orig[u][n]}" name={"sco"+str(u)+str(n)} id={"sco"+str(u)+str(n)}><br></td>''')
            table.append('</tr><br>')
        table=''.join(table)
    return TemplateResponse(request, 'scoring.html', locals())

"""
def scoring(request,team,week,num):
    if 'psw' not in request.session:
        return redirect("/teachlog/")
    no=request.session['psw']
    now=datetime.now()
    if request.method=="POST":
        try:
            w=Week.objects.get(name=week).__dict__
            team=Team.objects.get(name=team).__dict__
            user=User.objects.filter(team=team['id']).order_by('id')
            userv=User.objects.filter(team=team['id']).order_by('id').values()
            num1=request.POST["sco1"]
            b=biweekly.objects.filter(week=w['id'],stu=userv[0]['id'])
            if num==1:
                b.update(num1=num1)
            elif num==2:
                b.update(num2=num1)
            elif num==3:
                b.update(num3=num1)
            elif num==4:
                b.update(num4=num1)
            else:
                message='fu'
            if 'sco2' in request.POST:
                num2=request.POST["sco2"]
                b=biweekly.objects.filter(week=w['id'],stu=userv[1]['id'])
                if num==1:
                    b.update(num1=num2)
                if num==2:
                    b.update(num2=num2)
                if num==3:
                    b.update(num3=num2)
                if num==4:
                    b.update(num4=num2)
            if 'sco3' in request.POST:
                num3=request.POST["sco3"]
                b=biweekly.objects.filter(week=w['id'],stu=userv[2]['id'])
                if num==1:
                    b.update(num1=num3)
                if num==2:
                    b.update(num2=num3)
                if num==3:
                    b.update(num3=num3)
                if num==4:
                    b.update(num4=num3)
            if 'sco4' in request.POST:
                num4=request.POST["sco4"]
                b=biweekly.objects.filter(week=w['id'],stu=userv[3]['id'])
                if num==1:
                    b.update(num1=num3)
                if num==2:
                    b.update(num2=num3)
                if num==3:
                    b.update(num3=num3)
                if num==4:
                    b.update(num4=num3)
            return redirect('/teacher/')
        except:
            message='錯誤'
    else:
        w=Week.objects.get(name=week).__dict__
        team=Team.objects.get(name=team).__dict__
        user=User.objects.filter(team=team['id']).order_by('id')
        userv=User.objects.filter(team=team['id']).order_by('id').values()
        orig=[]
        for u in userv:
            b=biweekly.objects.filter(week=w['id'],stu=u['id']).values()
            if num==1:
                orig.append(b[0]['num1'])
            if num==2:
                orig.append(b[0]['num2'])
            if num==3:
                orig.append(b[0]['num3'])
            if num==4:
                orig.append(b[0]['num4'])


    return TemplateResponse(request, 'scoring.html', locals())"""

def delweek(request):
    if 'psw' not in request.session:
        return redirect("/teachlog/")
    no=request.session['psw']
    now=datetime.now()
    teamsum=Team.objects.all().aggregate(Count('name'))["name__count"]                    #這是組數
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]                    #week數
    teams=Team.objects.all().order_by('id').values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    memid=[]
    members=[]
    tolsum=[]
    sesuser=[]
    for j in range(teamsum):
        memid.append([])
        members.append([])
        tolsum.append([])
        sesuser.append([])

    for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id']).values()
                memid[j].append(locteamuser[k]['userid'])
                members[j].append(locteamuser[k]['name'])                                             #這 members 做出來是(組數，組員name)
                tolsum[j].append(0)

    for i in range(weeksum):
        tol.append([])
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            tol[i].append([])
            for k in range(mem):
                tol[i][j].append([])

    for i in range(weeksum):
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id'],week=weeks[i]['id']).order_by('num').values()
                for s in range(weeknums[i]):
                    tol[i][j][k].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
                    tolsum[j][k]=tolsum[j][k]+score[s]['sco']

    table1=[]
    for j in range(len(members)):
        table1.append(f'''<tr>
                    <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                    <td>{memid[j][0]}</td>
                    <td>{members[j][0]}</td>
                    ''')
        for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][0][b]}</td>')
        table1.append(f'<td>{tolsum[j][0]}</td></tr>')
        for i in range(1,len(members[j])):
            table1.append(f'''<tr>
            <td>{memid[j][i]}</td>
            <td>{members[j][i]}</td>
            ''')
            for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][i][b]}</td>')
            table1.append(f'<td>{tolsum[j][i]}</td></tr>')
        
    table1=''.join(table1)
    if request.method=="POST":
        try:
            weekid=request.POST["week"].strip()
            week=Week.objects.get(id=weekid)
            week.delete()
            
            return redirect("/teacher/")

        except:
            message='錯誤'
    else:
        weekna=[]
        weeks=Week.objects.all().order_by('id').values()
        for w in weeks:
            weekna.append((w['id'],w['name']))


    return TemplateResponse(request, 'delweek.html', locals())

def neweek(request):
    if 'psw' not in request.session:
        return redirect("/teachlog/")
    no=request.session['psw']
    now=datetime.now()
    teamsum=Team.objects.all().aggregate(Count('name'))["name__count"]                    #這是組數
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]                    #week數
    teams=Team.objects.all().order_by('id').values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    memid=[]
    members=[]
    tolsum=[]
    sesuser=[]
    for j in range(teamsum):
        memid.append([])
        members.append([])
        tolsum.append([])
        sesuser.append([])

    for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id']).values()
                memid[j].append(locteamuser[k]['userid'])
                members[j].append(locteamuser[k]['name'])                                             #這 members 做出來是(組數，組員name)
                tolsum[j].append(0)

    for i in range(weeksum):
        tol.append([])
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            tol[i].append([])
            for k in range(mem):
                tol[i][j].append([])

    for i in range(weeksum):
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id'],week=weeks[i]['id']).order_by('num').values()
                for s in range(weeknums[i]):
                    tol[i][j][k].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
                    tolsum[j][k]=tolsum[j][k]+score[s]['sco']

    table1=[]
    for j in range(len(members)):
        table1.append(f'''<tr>
                    <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                    <td>{memid[j][0]}</td>
                    <td>{members[j][0]}</td>
                    ''')
        for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][0][b]}</td>')
        table1.append(f'<td>{tolsum[j][0]}</td></tr>')
        for i in range(1,len(members[j])):
            table1.append(f'''<tr>
            <td>{memid[j][i]}</td>
            <td>{members[j][i]}</td>
            ''')
            for a in range(weeksum):
                for b in range(weeknums[a]):
                    table1.append(f'<td>{tol[a][j][i][b]}</td>')
            table1.append(f'<td>{tolsum[j][i]}</td></tr>')
        
    table1=''.join(table1)
    if request.method=="POST":
        form=forms.new_week(request.POST)
        if form.is_valid():
            try:
                name=request.POST["name"].strip()
                num=request.POST["num"]
                Week.objects.create(name=name,nums=num)
                week=Week.objects.get(name=name,nums=num)
                user=User.objects.all().order_by('id')
                for u in user:
                    for n in range(int(num)):
                        biweekly.objects.create(week=week,stu=u,num=n+1)
                return redirect("/teacher/")

            except:
                message='重複名稱'
    else:
        form=forms.new_week()
    #template=get_template("login.html")


    return TemplateResponse(request, 'neweek.html', locals())

def logout(request):
    now=datetime.now()
    request.session.pop("userid",None)
    request.session.pop("course",None)
    request.session.pop("name",None)
    return TemplateResponse(request, 'index.html', locals())

def userpro(request):
    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    else:
        redirect('/')
    now=datetime.now()
    userid=request.session['userid']
    course=request.session['course']
    name=request.session['name']
    user=User.objects.get(userid=userid)
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]     
    scors=biweekly.objects.filter(stu=user.id).values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    for i in range(weeksum):
        tol.append([])
        score=biweekly.objects.filter(stu=user.id,week=weeks[i]['id']).order_by('num').values()
        for s in range(weeknums[i]):
            tol[i].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
    aa=0
    for s in scors:
        aa+=s['sco']
    table=[]
    table.append('<tr>')
    for a in range(weeksum):
            for b in range(weeknums[a]):
                table.append(f'<td>{tol[a][b]}</td>')
    table.append(f'<td>{aa}</td></tr>')
    table=''.join(table)
    
    return TemplateResponse(request, 'userpro.html', locals())

def mypy(request):
    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    now=datetime.now()
    teamsum=Team.objects.all().aggregate(Count('name'))["name__count"]                    #這是組數
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]                    #week數
    teams=Team.objects.all().order_by('id').values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    memid=[]
    members=[]
    tolsum=[]
    sesuser=[]
    for j in range(teamsum):
        memid.append([])
        members.append([])
        tolsum.append([])
        sesuser.append([])

    for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id']).values()
                memid[j].append(locteamuser[k]['userid'])  
                members[j].append(locteamuser[k]['name'])                                             #這 members 做出來是(組數，組員name)
                tolsum[j].append(0)
                if 'userid' in request.session:
                    if locteamuser[k]['userid']==userid:
                        sesuser[j].append('style="background-color:#ff5555;"')
                    else:
                        sesuser[j].append('')

    for i in range(weeksum):
        tol.append([])
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            tol[i].append([])
            for k in range(mem):
                tol[i][j].append([])

    for i in range(weeksum):
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id']).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id']).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id'],week=weeks[i]['id']).order_by('num').values()
                for s in range(weeknums[i]):
                    tol[i][j][k].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
                    tolsum[j][k]=tolsum[j][k]+score[s]['sco']
  
    if 'userid' in request.session:
        table=[]
        for j in range(len(members)):
            table.append(f'''<tr {sesuser[j][0]}>
                        <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                        <td>{memid[j][0]}</td>
                        <td>{members[j][0]}</td>
                        ''')
            for a in range(weeksum):
                    for b in range(weeknums[a]):
                        table.append(f'<td>{tol[a][j][0][b]}</td>')
            table.append(f'<td>{tolsum[j][0]}</td></tr>')
            for i in range(1,len(members[j])):
                table.append(f'''<tr {sesuser[j][i]}>
                <td>{memid[j][i]}</td>
                <td>{members[j][i]}</td>
                ''')
                for a in range(weeksum):
                    for b in range(weeknums[a]):
                        table.append(f'<td>{tol[a][j][i][b]}</td>')
                table.append(f'<td>{tolsum[j][i]}</td></tr>')
            
        table=''.join(table)
    else:
        table=[]
        for j in range(len(members)):
            table.append(f'''<tr>
                        <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                        <td>{memid[j][0]}</td>
                        <td>{members[j][0]}</td>
                        ''')
            for a in range(weeksum):
                    for b in range(weeknums[a]):
                        table.append(f'<td>{tol[a][j][0][b]}</td>')
            table.append(f'<td>{tolsum[j][0]}</td></tr>')
            for i in range(1,len(members[j])):
                table.append(f'''<tr>
                <td>{memid[j][i]}</td>
                <td>{members[j][i]}</td>
                ''')
                for a in range(weeksum):
                    for b in range(weeknums[a]):
                        table.append(f'<td>{tol[a][j][i][b]}</td>')
                table.append(f'<td>{tolsum[j][i]}</td></tr>')
            
        table=''.join(table)



    return TemplateResponse(request, 'mypy.html', locals())

def searchname(request):

    search=request.GET.get('v')
    if search==None:
        search=""
    searchid=request.GET.get('v2')
    if searchid==None:
        searchid=""

    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    now=datetime.now()
    teamsum=Team.objects.all().aggregate(Count('name'))["name__count"]                    #這是組數
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]                    #week數
    teams=Team.objects.all().order_by('id').values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    memid=[]
    members=[]
    tolsum=[]
    sesuser=[]
    for j in range(teamsum):
        memid.append([])
        members.append([])
        tolsum.append([])
        sesuser.append([])

    for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id'],name__contains=search,userid__contains=searchid).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id'],name__contains=search,userid__contains=searchid).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id']).values()
                memid[j].append(locteamuser[k]['userid'])     
                members[j].append(locteamuser[k]['name'])                                             #這 members 做出來是(組數，組員name)
                tolsum[j].append(0)
                if 'userid' in request.session:
                    if locteamuser[k]['userid']==userid:
                        sesuser[j].append('style="background-color:#ff5555;"')
                    else:
                        sesuser[j].append('')

    for i in range(weeksum):
        tol.append([])
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id'],name__contains=search,userid__contains=searchid).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id'],name__contains=search,userid__contains=searchid).aggregate(Count('name'))["name__count"]
            tol[i].append([])
            for k in range(mem):
                tol[i][j].append([])

    for i in range(weeksum):
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id'],name__contains=search,userid__contains=searchid).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id'],name__contains=search,userid__contains=searchid).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id'],week=weeks[i]['id']).order_by('num').values()
                for s in range(weeknums[i]):
                    tol[i][j][k].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
                    tolsum[j][k]=tolsum[j][k]+score[s]['sco']
  
    if 'userid' in request.session:
        table=[]
        for j in range(len(members)):
            try:
                table.append(f'''<tr {sesuser[j][0]}>
                            <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                            <td>{memid[j][0]}</td>
                            <td>{members[j][0]}</td>
                            ''')
                for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][0][b]}</td>')
                table.append(f'<td>{tolsum[j][0]}</td></tr>')
                for i in range(1,len(members[j])):
                    table.append(f'''<tr {sesuser[j][i]}>
                    <td>{memid[j][i]}</td>
                    <td>{members[j][i]}</td>
                    ''')
                    for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][i][b]}</td>')
                    table.append(f'<td>{tolsum[j][i]}</td></tr>')
            except:
                pass
            
        table=''.join(table)
    else:
        table=[]
        for j in range(len(members)):
            try:
                table.append(f'''<tr>
                            <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                            <td>{memid[j][0]}</td>
                            <td>{members[j][0]}</td>
                            ''')
                for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][0][b]}</td>')
                table.append(f'<td>{tolsum[j][0]}</td></tr>')
                for i in range(1,len(members[j])):
                    table.append(f'''<tr>
                    <td>{memid[j][i]}</td>
                    <td>{members[j][i]}</td>
                    ''')
                    for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][i][b]}</td>')
                    table.append(f'<td>{tolsum[j][i]}</td></tr>')
            except:
                pass
            
        table=''.join(table)
    res=0
    for j in range(len(members)):
        res+=len(members[j])
    wee=0
    for w in weeks:
        wee+=w['nums']
    if res==0:
        table=f'''<tr><td colspan="{wee+4}">查無資料</td></tr>'''

    return JsonResponse({'res': table})

def searchid(request):

    search=request.GET.get('v')

    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    now=datetime.now()
    teamsum=Team.objects.all().aggregate(Count('name'))["name__count"]                    #這是組數
    weeksum=Week.objects.all().aggregate(Count('name'))["name__count"]                    #week數
    teams=Team.objects.all().order_by('id').values()
    weeks=Week.objects.all().order_by('id').values()
    weeknums=[]
    for w in weeks:
        weeknums.append(w['nums'])
    tol=[]
    memid=[]
    members=[]
    tolsum=[]
    sesuser=[]
    for j in range(teamsum):
        memid.append([])
        members.append([])
        tolsum.append([])
        sesuser.append([])

    for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id'],userid__contains=search).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id'],userid__contains=search).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id']).values()
                memid[j].append(locteamuser[k]['userid'])     
                members[j].append(locteamuser[k]['name'])                                             #這 members 做出來是(組數，組員name)
                tolsum[j].append(0)
                if 'userid' in request.session:
                    if locteamuser[k]['userid']==userid:
                        sesuser[j].append('style="background-color:#ff5555;"')
                    else:
                        sesuser[j].append('')

    for i in range(weeksum):
        tol.append([])
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id'],userid__contains=search).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id'],userid__contains=search).aggregate(Count('name'))["name__count"]
            tol[i].append([])
            for k in range(mem):
                tol[i][j].append([])

    for i in range(weeksum):
        for j in range(teamsum):
            locteamuser=User.objects.filter(team=teams[j]['id'],userid__contains=search).order_by('id').values()
            mem=User.objects.filter(team=teams[j]['id'],userid__contains=search).aggregate(Count('name'))["name__count"]
            for k in range(mem):
                score=biweekly.objects.filter(stu=locteamuser[k]['id'],week=weeks[i]['id']).order_by('num').values()
                for s in range(weeknums[i]):
                    tol[i][j][k].append(score[s]['sco'])          #這 tol 做出來是(週數，組數，組員樹，四題的分數)
                    tolsum[j][k]=tolsum[j][k]+score[s]['sco']
  
    if 'userid' in request.session:
        table=[]
        for j in range(len(members)):
            try:
                table.append(f'''<tr {sesuser[j][0]}>
                            <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                            <td>{memid[j][0]}</td>
                            <td>{members[j][0]}</td>
                            ''')
                for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][0][b]}</td>')
                table.append(f'<td>{tolsum[j][0]}</td></tr>')
                for i in range(1,len(members[j])):
                    table.append(f'''<tr {sesuser[j][i]}>
                    <td>{memid[j][i]}</td>
                    <td>{members[j][i]}</td>
                    ''')
                    for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][i][b]}</td>')
                    table.append(f'<td>{tolsum[j][i]}</td></tr>')
            except:
                pass
            
        table=''.join(table)
    else:
        table=[]
        for j in range(len(members)):
            try:
                table.append(f'''<tr>
                            <th rowspan={len(members[j])}>{teams[j]['name']}</th>
                            <td>{memid[j][0]}</td>
                            <td>{members[j][0]}</td>
                            ''')
                for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][0][b]}</td>')
                table.append(f'<td>{tolsum[j][0]}</td></tr>')
                for i in range(1,len(members[j])):
                    table.append(f'''<tr>
                    <td>{memid[j][i]}</td>
                    <td>{members[j][i]}</td>
                    ''')
                    for a in range(weeksum):
                        for b in range(weeknums[a]):
                            table.append(f'<td>{tol[a][j][i][b]}</td>')
                    table.append(f'<td>{tolsum[j][i]}</td></tr>')
            except:
                pass
            
        table=''.join(table)



    return JsonResponse({'res': table})


def myml(request):
    if 'userid' in request.session:
        userid=request.session['userid']
        course=request.session['course']
        name=request.session['name']
    now=datetime.now()
    return TemplateResponse(request, 'myml.html', locals())

def chat(request):
    c=request.GET.get('v')
    chatmes.objects.create(text=str(c))
    return JsonResponse({'res': c})

def chatroom(request):
    chatmess=chatmes.objects.all().order_by('id').values()
    html=''
    for i in chatmess:
        html+=f"<p>{i['text']}</p><br>"

    return JsonResponse({'res': html})

def chatsite(request):
    now=datetime.now()

    return TemplateResponse(request, 'chat.html', locals())
def clearchat(request):
    chatmess=chatmes.objects.all()
    for c in chatmess:
        c.delete()

def test(request):
    now=datetime.now()
    return TemplateResponse(request, 'test.html', locals())
def testadd(request):
    v=request.GET.get('v')
    now=datetime.now()
    return JsonResponse({'res':v+'py'})