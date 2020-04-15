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








    # a = Team.objects.all()
    # temp = []
    # for i in a:
    #     test = i.files.all()
    #     for j in test:
    #         if request.user == j.member:
    #             if j.is_active == True:
    #                 temp.append(j.team)
    teammember = TeamMembers.objects.filter(member=request.user).all()
    # teammember = TeamMembers.objects.filter(member=request.user, member_status="Leader").all()
    b = TeamMembers.objects.all()

    team_my = Team.objects.all().filter(user=request.user)
    result_my = []
    for field in team_my:
        if field.end_time.date() < datetime.datetime.now().date():
            pass
        else:
            result_my.append(field.files.all()[0])



    # team = Team.objects.all().filter(user=request.user)
    search = request.GET.get('search')



    team_data = Team.objects.all()
    team = []
    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:
                team.append(i)


    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)


    result_required = []



    result = []
    for field in team:
        if field.end_time.date() < datetime.datetime.now().date():
            pass
        else:
            result.append(field.files.all()[0])
            # for i in field.files.all():
            #     result.append(i)
        if field.end_time.date() == tomorrow.date():
            result_required.append(field.files.all()[0])

            # for i in field.files.all():
            #     result_required.append(i)

    context['team'] = result
    context['countall'] = len(result)
    context['countmy'] =len(result_my)

    context['countrequired'] = len(result_required)



    if search:
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
        files = request.FILES.getlist('thumbnail')
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

            for f in files:

                gallery = TeamDocuments(team_id=article, document=f)
                gallery.save()
            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager:
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
            print(assinger)
            print('ASGHJRHGDFKM<')
            # member = ''
            if assinger and position:

                i = 0
                for user in assinger:


                    email = MyUser.objects.filter(email=user).last()
                    if email:

                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i +=1

                        print('CREATED MEMBER!!!')
            # article.save()
        return redirect(dashboard)
    return render(request, 'dashboard.html', context)




def dashboard_edit(request,id):
    # if request.is_ajax:
    teammember = TeamMembers.objects.filter(id=id).first()
    team = teammember.team
    document = TeamDocuments.objects.filter(team_id=team)
    picture = team.team_picture
    members =  teammember.team.files.all().exclude(member_status='Leader')
    leader = teammember.team.files.all().filter(member_status='Leader')[0]



    form = CreateTeam(instance=team)
    context = {
        'form' : form,
        'picture' : picture,
        'files' : document,
        'members': members,
        'leader': leader,
        'teammember' : teammember
    }

    if request.method == 'POST':


        form = CreateTeam(request.POST, request.FILES,instance=team)
        files = request.FILES.getlist('thumbnail')
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

            for f in files:
                gallery = TeamDocuments(team_id=article, document=f)
                gallery.save()

            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            # return HttpResponse(assinger)
            for i in team.files.all():
                i.delete()

            if manager:
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

            if assinger and position:

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
    # a = Team.objects.all()
    # temp = []
    # for i in a:
    #     test = i.files.all()
    #     for j in test:
    #         if request.user == j.member:
    #             if j.is_active == True:
    #                 temp.append(j.team)
    teammember = TeamMembers.objects.filter(member=request.user,member_status="Leader").all()
    # context['team'] = teammember
    b = TeamMembers.objects.all()
    context['test'] = list(b)

    team_data = Team.objects.all()
    team_list = []
    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:
                team_list.append(i)

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

    result_required = []



    result_all = []
    for field in team_list:
        if field.end_time.date() < datetime.datetime.now().date():
            pass
        else:
            result_all.append(field.files.all()[0])
            # for i in field.files.all():
            #     result.append(i)
        if field.end_time.date() == tomorrow.date():
            result_required.append(field.files.all()[0])



    search = request.GET.get('search')
    if search:
        team = Team.objects.filter(
            Q(team_name__icontains=search) &
            Q(user=request.user)

        )


    else:
        team = Team.objects.all().filter(user=request.user)

    result = []
    for field in team:
        if field.end_time.date() < datetime.datetime.now().date():
            pass
        else:
            result.append(field.files.all()[0])
            # for i in field.files.all():
            #     result.append(i)
    context['team'] = result
    context['countall'] = len(result_all)
    context['countmy'] = len(result)

    context['countrequired'] = len(result_required)
    team_data = Team.objects.all()
    team = []
    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:
                team.append(i)

    if request.method == 'POST':
        form = CreateTeam(request.POST, request.FILES)
        files = request.FILES.getlist('thumbnail')
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

            for f in files:
                gallery = TeamDocuments(team_id=article, document=f)
                gallery.save()
            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager:
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
            print(assinger)
            print('ASGHJRHGDFKM<')
            # member = ''
            i = 0

            if assinger and position:

                for user in assinger:

                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i += 1

                        print('CREATED MEMBER!!!')
            # article.save()
        return redirect(dashboard)

    return render(request, 'dashboard.html', context)



def required_project(request):
    context = {}
    context['form'] = CreateTeam()
    # a = Team.objects.all()
    # temp = []
    # for i in a:
    #     test = i.files.all()
    #     for j in test:
    #         if request.user == j.member:
    #             if j.is_active == True:
    #                 temp.append(j.team)
    teammember = TeamMembers.objects.filter(member=request.user, member_status="Leader").all()
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

    search = request.GET.get('search')


    team_data = Team.objects.all()

    team_list = []
    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:
                team_list.append(i)

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

    result_required = []

    result_all = []
    for field in team_list:
        if field.end_time.date() < datetime.datetime.now().date():
            pass
        else:
            result_all.append(field.files.all()[0])
            # for i in field.files.all():
            #     result.append(i)
        if field.end_time.date() == tomorrow.date():
            result_required.append(field.files.all()[0])

    team = Team.objects.all().filter(user=request.user)
    result = []
    for field in team:
        if field.end_time.date() < datetime.datetime.now().date():
            pass
        else:
            result.append(field.files.all()[0])
            # for i in field.files.all():
            #     result.append(i)
    context['team'] = result_required
    context['countall'] = len(result_all)
    context['countmy'] = len(result)

    context['countrequired'] = len(result_required)


    if search:
        team_data = Team.objects.filter(
            Q(team_name__icontains=search)

        )

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













    b = TeamMembers.objects.all()
    context['test'] = list(b)
    if request.method == 'POST':
        form = CreateTeam(request.POST, request.FILES)
        files = request.FILES.getlist('thumbnail')
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

            for f in files:
                gallery = TeamDocuments(team_id=article, document=f)
                gallery.save()
            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager:
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
            print(assinger)
            print('ASGHJRHGDFKM<')
            # member = ''
            i = 0

            if assinger and position:

                for user in assinger:

                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i += 1

                        print('CREATED MEMBER!!!')
            # article.save()
        return redirect(dashboard)

    return render(request, 'dashboard.html', context)


def finished_project(request):
    context = {}
    context['form'] = CreateTeam()
    # a = Team.objects.all()
    # temp = []
    # for i in a:
    #     test = i.files.all()
    #     for j in test:
    #         if request.user == j.member:
    #             if j.is_active == True:
    #                 temp.append(j.team)
    teammember = TeamMembers.objects.filter(member=request.user,member_status="Leader").all()

    search = request.GET.get('search')



    team_data = Team.objects.all()

    team_list = []
    for i in team_data:
        for member in i.files.all():
            if member.member == request.user:
                team_list.append(i)

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)

    result_required = []
    result_finish = []
    result_all = []
    for field in team_list:
        if field.end_time.date() < datetime.datetime.now().date():
            result_finish.append(field.files.all()[0])
        else:
            result_all.append(field.files.all()[0])
            # for i in field.files.all():
            #     result.append(i)
        if field.end_time.date() == tomorrow.date():
            result_required.append(field.files.all()[0])

    team = Team.objects.all().filter(user=request.user)
    result = []
    for field in team:
        if field.end_time.date() < datetime.datetime.now().date():
            pass
        else:
            result.append(field.files.all()[0])
            # for i in field.files.all():
            #     result.append(i)
    context['team'] = result_required
    context['countall'] = len(result_all)
    context['countmy'] = len(result)
    context['countrequired'] = len(result_required)
    context['team'] = result_finish

    if search:
        team_data = Team.objects.filter(
            Q(team_name__icontains=search)

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


    # team = Team.objects.all().filter(user=request.user)
    # result_finish = []
    # for field in team:
    #     if field.end_time.date() < datetime.datetime.now().date():
    #         result_finish.append(field.files.all()[0])
    #
    #














    b = TeamMembers.objects.all()
    context['test'] = list(b)
    if request.method == 'POST':
        form = CreateTeam(request.POST, request.FILES)
        files = request.FILES.getlist('thumbnail')
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

            for f in files:
                gallery = TeamDocuments(team_id=article, document=f)
                gallery.save()
            assinger = request.POST.getlist('assinger')
            position = request.POST.getlist('position')
            manager = request.POST.get('manager')

            if manager:
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
            print(assinger)
            print('ASGHJRHGDFKM<')
            # member = ''
            i = 0

            if assinger and position:

                for user in assinger:

                    email = MyUser.objects.filter(email=user).last()
                    if email:
                        TeamMembers.objects.create(team=article, member=email, member_status=position[i])
                        i += 1

                        print('CREATED MEMBER!!!')
            # article.save()
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


