from django.contrib import messages
from django.shortcuts import render, redirect
from teams_app.forms import CreateTeam, CreateMember
from teams_app.models import Team, TeamMembers, TokenModelTeam,TeamDocuments
from user_app.models import MyUser
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import  datetime

# Create your views here.



def dashboard(request):
    context = {}
    context['form'] = CreateTeam()

    b = TeamMembers.objects.all()

    team_my = Team.objects.all().filter(user=request.user)
    result_my = []


    for field in team_my:
        if field.end_time.date() >= datetime.datetime.now().date():  # MY ACTIVE PROJECTS  TEAM LEAD OLDUGUM PROJECTLER
            result_my.append(field.files.all()[0])


    team_data = Team.objects.all()
    team = []


    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:
                team.append(i)                              # ASSIGN OLDUGUM BUTUN PROJECTLER


    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)


    result_required = []
    result = []


    for field in team:
        if field.end_time.date() >= datetime.datetime.now().date():   # ASSIGN OLDUGUM ACTIVE PROJECTLER
            result.append(field.files.all()[0])

        if field.end_time.date() == tomorrow.date():        # ASSIGN OLDUGUM DEADLINE A 1 GUN QALMIS PROJECTLER
            result_required.append(field.files.all()[0])


    context['team'] = result
    context['countall'] = len(result)
    context['countmy'] =len(result_my)
    context['countrequired'] = len(result_required)

    search = request.GET.get('search')

    if search:                                 # SEARCH HISSE YENIDEN FILTER
        team_data = Team.objects.filter(
            Q(team_name__icontains=search)

        )
        team = []
        for i in team_data:
            for member in i.files.all():
                if member.member == request.user:
                    team.append(i)

        result = []
        for field in team:
            if field.end_time.date() >= datetime.datetime.now().date():
                result.append(field.files.all()[0])

        context['team'] = result
        context['countall'] = len(result)

    context['test'] = list(b)





    if request.method == 'POST':
        form = CreateTeam(request.POST, request.FILES)
        if form.is_valid():
            picture = request.FILES.get('team_picture')

            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            article = form.save(commit=False)

            article.start_time = start
            article.end_time = end
            article.user = request.user
            article.team_picture = picture
            article.save()

            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager:     # TEAM LEAD SET
                verify_manager = MyUser.objects.filter(email=manager).last()
                if verify_manager:
                    TeamMembers.objects.create(team=article, member=verify_manager,
                                               member_status='Leader', is_active=True)
                    article.user=verify_manager
                    article.save()
            else:
                TeamMembers.objects.create(team=article, member=article.user,
                                               member_status='Leader', is_active=True)

            print("CREATED TEAM LEADER!")




            if assinger and position:      # ASSIGNERS AND POSITION SET
                i = 0
                for user in assinger:
                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i +=1
                        print('CREATED MEMBER!!!')
        return redirect(dashboard)
    return render(request, 'dashboard.html', context)




def dashboard_edit(request,id):
    teammember = TeamMembers.objects.filter(id=id).first()
    team = Team.objects.all().filter(id=id).first()

    document = TeamDocuments.objects.filter(team_id=team)
    picture = team.team_picture
    members = team.files.all().exclude(member_status='Leader')
    leader = team.files.all().filter(member_status='Leader')[0]



    form = CreateTeam(instance=team)
    context = {
        'form' : form,
        'picture' : picture,
        'files' : document,
        'members': members,
        'leader': leader,
        'teammember' : team
    }

    if request.method == 'POST':


        form = CreateTeam(request.POST, request.FILES,instance=team)
        if form.is_valid():
            picture = request.FILES.get('team_picture')
            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            article = form.save(commit=False)

            article.start_time = start
            article.end_time = end
            article.user = request.user
            if picture:
                article.team_picture = picture
            article.save()



            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            for i in team.files.all():     # ASSIGN OLAN USERLERI SILIB YENIDEN YARADIRAM
                i.delete()

            if manager:         # TEAMLEAD SET
                verify_manager = MyUser.objects.filter(email=manager).last()
                if verify_manager:
                    TeamMembers.objects.create(team=article, member=verify_manager,
                                               member_status='Leader', is_active=True)
                    article.user=verify_manager
                    article.save()
            else:
                TeamMembers.objects.create(team=article, member=article.user,
                                               member_status='Leader', is_active=True)

            i = 0

            if assinger and position:     # ASSIGNERS AND POSITION SET

                for user in assinger:

                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i += 1

                        print('CREATED MEMBER!!!')


            return redirect('dashboard')

    return render(request,"dashboard-edit.html",context)


def active_my(request):
    context = {}
    context['form'] = CreateTeam()

    b = TeamMembers.objects.all()

    team_data = Team.objects.all()

    team_list = []

    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:     # ASSIGN OLDUGUM BUTUN PROJECTLER
                team_list.append(i)

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

    result_required = []



    result_all = []
    for field in team_list:
        if field.end_time.date() >= datetime.datetime.now().date():   # ASSIGN OLDUGUM ACTIVE PROJECTLER
            result_all.append(field.files.all()[0])

        if field.end_time.date() == tomorrow.date():
            result_required.append(field.files.all()[0])   # REQUIRED PROJECTLER



    search = request.GET.get('search')
    if search:                                     # SEARCH HISSE FILTER
        team = Team.objects.filter(
            Q(team_name__icontains=search) &
            Q(user=request.user)

        )


    else:
        team = Team.objects.all().filter(user=request.user)

    result = []
    for field in team:
        if field.end_time.date() >= datetime.datetime.now().date():   # TEAMLEAD OLDUGUM ACTIVE PORJECTLER
            result.append(field.files.all()[0])

    context['team'] = result
    context['countall'] = len(result_all)
    context['countmy'] = len(result)

    context['countrequired'] = len(result_required)


    if request.method == 'POST':
        form = CreateTeam(request.POST, request.FILES)
        if form.is_valid():
            picture = request.FILES.get('team_picture')

            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            article = form.save(commit=False)

            article.start_time = start
            article.end_time = end
            article.user = request.user
            article.team_picture = picture
            article.save()


            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager: # TEAMLEAD SET
                verify_manager = MyUser.objects.filter(email=manager).last()
                if verify_manager:
                    TeamMembers.objects.create(team=article, member=verify_manager,
                                               member_status='Leader', is_active=True)
                    article.user = verify_manager
                    article.save()
            else:
                TeamMembers.objects.create(team=article, member=article.user,
                                           member_status='Leader', is_active=True)

            print("CREATED TEAM LEADER!")

            i = 0

            if assinger and position:      #ASSIGN POSITION SET

                for user in assinger:

                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i += 1

                        print('CREATED MEMBER!!!')
        return redirect(dashboard)

    return render(request, 'dashboard.html', context)



def required_project(request):
    context = {}
    context['form'] = CreateTeam()
    team_data = Team.objects.all()

    team_list = []
    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:        # ASSIGN OLDUGUM BUTUN PROJECTLER
                team_list.append(i)

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

    result_required = []

    result_all = []
    for field in team_list:
        if field.end_time.date() >= datetime.datetime.now().date(): # ASSIGN OLDUGUM ACTIVE PROJECTLER
            result_all.append(field.files.all()[0])

        if field.end_time.date() == tomorrow.date():    # REQUIRED PROJECTLER
            result_required.append(field.files.all()[0])

    team = Team.objects.all().filter(user=request.user)
    result = []

    for field in team:
        if field.end_time.date() >= datetime.datetime.now().date():  # TEAMLEAD OLDUGUM ACTIVE PROJECTLER
            result.append(field.files.all()[0])

    context['team'] = result_required
    context['countall'] = len(result_all)
    context['countmy'] = len(result)

    context['countrequired'] = len(result_required)


    search = request.GET.get('search')


    if search:
        team_data = Team.objects.filter(
            Q(team_name__icontains=search)

        )
                                        # SEARCH FILTER

        team_list = []
        for i in team_data:
            for member in i.files.all():
                if member.member == request.user:
                    team_list.append(i)

        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

        result_search = []

        result_all = []
        for field in team_list:

            if field.end_time.date() == tomorrow.date():
                result_search.append(field.files.all()[0])

        context['team'] = result_search
        context['countrequired'] = len(result_search)

    if request.method == 'POST':
        form = CreateTeam(request.POST, request.FILES)
        if form.is_valid():
            picture = request.FILES.get('team_picture')

            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            article = form.save(commit=False)

            article.start_time = start
            article.end_time = end
            article.user = request.user
            article.team_picture = picture
            article.save()


            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager:    # TEAMLEAD SET
                verify_manager = MyUser.objects.filter(email=manager).last()
                if verify_manager:
                    TeamMembers.objects.create(team=article, member=verify_manager,
                                               member_status='Leader', is_active=True)
                    article.user = verify_manager
                    article.save()
            else:
                TeamMembers.objects.create(team=article, member=article.user,
                                           member_status='Leader', is_active=True)

            print("CREATED TEAM LEADER!")

            i = 0

            if assinger and position:      # ASSIGNERS SET

                for user in assinger:

                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i += 1

                        print('CREATED MEMBER!!!')
        return redirect(dashboard)

    return render(request, 'dashboard.html', context)


def finished_project(request):
    context = {}
    context['form'] = CreateTeam()

    team_data = Team.objects.all()

    team_list = []
    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:   # ASSIGN OLDUGUM BUTUN PROJECTLER
                team_list.append(i)

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

    result_required = []
    result_finish = []
    result_all = []
    for field in team_list:
        if field.end_time.date() < datetime.datetime.now().date():   #ASSIGN OLDUGUM ACTIVE PROJECTLER
            result_finish.append(field.files.all()[0])
        else:                                            # ASSIGN OLDUGUM BITMIS PROJECTLER
            result_all.append(field.files.all()[0])

        if field.end_time.date() == tomorrow.date():          # ASSIGN OLDUGUM REQUIRED PROJECTLER
            result_required.append(field.files.all()[0])

    team = Team.objects.all().filter(user=request.user)
    result = []
    for field in team:
        if field.end_time.date() >= datetime.datetime.now().date(): # TEAMLEAD OLDUGUM ACTIVE PROJECTLER
            result.append(field.files.all()[0])

    context['team'] = result_required
    context['countall'] = len(result_all)
    context['countmy'] = len(result)
    context['countrequired'] = len(result_required)
    context['team'] = result_finish


    search = request.GET.get('search')

    if search:
        team_data = Team.objects.filter(
            Q(team_name__icontains=search)      # SEARCH FILTER

        )

        result_search = []

        team_list = []
        for i in team_data:
            for member in i.files.all():
                if member.member == request.user:
                    team_list.append(i)

        for field in team_list:
            if field.end_time.date() < datetime.datetime.now().date():
                result_search.append(field.files.all()[0])

        context['team'] = result_search



    if request.method == 'POST':
        form = CreateTeam(request.POST, request.FILES)
        if form.is_valid():
            picture = request.FILES.get('team_picture')

            start = form.cleaned_data['start_time']
            end = form.cleaned_data['end_time']
            article = form.save(commit=False)

            article.start_time = start
            article.end_time = end
            article.user = request.user
            article.team_picture = picture
            article.save()


            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager:    # TEAMLEAD SET
                verify_manager = MyUser.objects.filter(email=manager).last()
                if verify_manager:
                    TeamMembers.objects.create(team=article, member=verify_manager,
                                               member_status='Leader', is_active=True)
                    article.user = verify_manager
                    article.save()
            else:
                TeamMembers.objects.create(team=article, member=article.user,
                                           member_status='Leader', is_active=True)

            print("CREATED TEAM LEADER!")

            i = 0

            if assinger and position:
                                              # ASSIGNERS AND POSITION SET
                for user in assinger:

                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i += 1

                        print('CREATED MEMBER!!!')
        return redirect(dashboard)

    return render(request, 'dashboard.html', context)




def detail_team(request, id):

    data = Team.objects.filter(id=id).first()

    members = data.files.all().exclude(member_status='Leader')
    leader = data.files.all().filter(member_status='Leader').first()

    context = {
        'data' : data,
        'members': members,
        'leader' : leader
    }

    return render(request, 'detail.html', context)


def verify_view(request, token, id):
    print('JOINED VERIFY')
    verify = TokenModelTeam.objects.filter(
        token=token,
        expired=False,
        user_id=id
    ).last()
    print(verify)
    if verify:
        a = TeamMembers.objects.filter(member_id=id).last()
        a.is_active = True
        a.save()
        verify.expired = True
        verify.save()
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        return redirect('myteams')
    else:
        print('---------------------------------------------')
        return redirect('index')


def delete_project(request, id):
    return JsonResponse({
        'sd' : 'sdfg'
    })