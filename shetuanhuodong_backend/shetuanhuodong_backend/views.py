from django.shortcuts import render
# from django import HttpResponse
from django.http import HttpResponse
import MySQLdb
from back_end.models import users
from back_end.models import teams
from back_end.models import activities
from back_end.models import nickname

import json


# Create your views here.
def login(request):
    db = MySQLdb.connect(user="yang", db="back_end", password="yang", host="localhost")
    cursor = db.cursor()
    json_dic = eval(request.body)
    username = json_dic['username']
    password = json_dic['password']
    sql = "select password from back_end_users where user_name='{0}'".format(username)
    cursor.execute(sql)
    dbpassword = cursor.fetchone()
    if password == dbpassword[0]:
        return HttpResponse('true')
    else:
        return HttpResponse('false')
    db.close()


def register(request):
    import datetime
    json_dic = eval(request.body)
    username = json_dic['username']
    password = json_dic['password']
    phone_number = json_dic['phone_number']
    create_time = datetime.datetime.now()
    try:
        user = users(user_name=username, password=password, create_time=create_time, phone_number=phone_number)
        user.save()
    except Exception as err:
        return HttpResponse(err)
    else:
        return HttpResponse('true')
    db.close()


def home(request):
    import datetime
    json_dic = eval(request.body)
    username = json_dic['username']
    user_activity = []
    try:
        user_activity = users.objects.get(user_name=username).activities.split(',')
    except:
        pass
    activity_info = []
    for i in user_activity:
        try:
            activity_time = str(activities.objects.get(name=i, status=1).time.date())
        except:
            pass
        else:
            activity_info.append((i, activity_time))
    return HttpResponse(json.dumps(activity_info), content_type='application/json')


def activity(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    return HttpResponse('1')


def team(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    user_friends = []
    user_teams = []
    to_add_friends = []
    try:
        user_friends = users.objects.get(user_name=username).friends.split(',')
    except:
        pass
    try:
        user_teams = users.objects.get(user_name=username).teams.split(',')
    except:
        pass
    to_add_friends = users.objects.get(user_name=username).to_add_friends.split(',')
    for i in to_add_friends:
        if not i:
            to_add_friends.remove(i)
    for i in range(len(to_add_friends)):
        item = to_add_friends[i].split(';')
        to_add_friends[i] = item
    result = [user_friends, user_teams, to_add_friends]
    return HttpResponse(json.dumps(result), content_type='application/json')


def me(request):
    import datetime
    json_dic = eval(request.body)
    username = json_dic['username']
    user_create_time = users.objects.get(user_name=username).create_time.date()
    return HttpResponse(user_create_time)


def activity_info(request):
    import datetime
    json_dic = eval(request.body)
    activity_name = json_dic['activity']
    activity = activities.objects.get(name=activity_name)
    team = activity.team
    if not team:
        team = '无'
    activity_users = []
    try:
        activity_users = activities.objects.get(name=activity_name).participants.split(',')
    except:
        pass
    activity_dic = {'name': activity_name,
                    'time': str(activity.time.date()),
                    'location': activity.location,
                    'content': activity.content,
                    'requirement': activity.requirement,
                    'launcher': activity.launcher,
                    'team': team,
                    'activity_users': activity_users
                    }
    return HttpResponse(json.dumps(activity_dic), content_type='application/json')


def sign_out_activity(request):
    json_dic = eval(request.body)
    activity = json_dic['activity']
    user_name = json_dic['user_name']
    user_activity = users.objects.get(user_name=user_name).activities.split(',')
    new_user_activity = ''
    for i in range(len(user_activity)):
        if user_activity[i] == activity:
            user_activity.remove(user_activity[i])
            break
    for j in range(len(user_activity)):
        if j != 0:
            new_user_activity += ',' + user_activity[j]
        if j == 0:
            new_user_activity += user_activity[j]
    users.objects.filter(user_name=user_name).update(activities=new_user_activity)

    activity_participants = activities.objects.get(name=activity).participants.split(',')
    new_activity_participants = ''
    for i in range(len(activity_participants)):
        if activity_participants[i] == user_name:
            activity_participants.remove(activity_participants[i])
            break

    for j in range(len(activity_participants)):
        if j != 0:
            new_activity_participants += ',' + activity_participants[j]
        if j == 0:
            new_activity_participants += activity_participants[j]
    activities.objects.filter(name=activity).update(participants=new_activity_participants)
    return HttpResponse("deleted")

def launch_activity(request):
    json_dic = eval(request.body)
    activity = json_dic['activity']
    time = json_dic['time']
    location = json_dic['location']
    content = json_dic['content']
    requirement = json_dic['requirement']
    launcher = json_dic['launcher']
    team = json_dic['team']
    try:
        new_activity = activities.objects.create(name=activity,
                                  time=time,
                                  location=location,
                                  content=content,
                                  requirement=requirement,
                                  launcher=launcher,
                                  participants=launcher)
        new_activity.save()
        if team != '无':
            activities.objects.filter(name=activity).update(team=team)
            team_activities = []
            try:
                team_activities = teams.objects.get(team_name=team_name).activities.split(',')
            except:
                pass
            team_activities.append(activity)
            new_team_activities = ''
            for i in range(len(team_activities)):
                if i != 0:
                    new_team_activities += ',' + team_activities[i]
                if i == 0:
                    new_team_activities += team_activities[i]
            teams.objects.filter(team_name=team).update(activities=new_team_activities)

        user_activity = users.objects.get(user_name=launcher).activities.split(',')
        user_activity = list(user_activity)
        user_activity.append(activity)
        new_user_activity = ''
        for i in range(len(user_activity)):
            if i != 0:
                new_user_activity += ',' + user_activity[i]
            if i == 0:
                new_user_activity += user_activity[i]
        users.objects.filter(user_name=launcher).update(activities=new_user_activity)

        return HttpResponse('1')
    except Exception as err:
        return HttpResponse(err)


def personal_info(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    user_gender = users.objects.get(user_name=username).sex
    user_introduction = users.objects.get(user_name=username).self_introduction
    whether_upload = False
    if users.objects.get(user_name=username).time_schedule:
        whether_upload = True
    dic = {
        'user_gender': user_gender,
        'user_introduction': user_introduction,
        'whether_upload': whether_upload
    }
    return HttpResponse(json.dumps(dic), content_type='application/json')


def change_name(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    new_username = json_dic['new_username']
    users.objects.filter(user_name=username).update(user_name=new_username)
    nick_name = nickname.object.get(user_name=username).nick_name
    if nick_name == username:
        nickname.object.filter(user_name=username).update(nick_name=new_username)
    return HttpResponse('true')


def change_introduction(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    introduction = json_dic['introduction']
    users.objects.filter(user_name=username).update(self_introduction=introduction)
    return HttpResponse('true')


def change_sex(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    sex = json_dic['sex']
    users.objects.filter(user_name=username).update(sex=sex)
    return HttpResponse('true')


def fetch_load(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    time_data = users.objects.get(user_name=username).time_schedule
    return HttpResponse(json.dumps(time_data), content_type='application/json')


def upload(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    time_data = json_dic['time_data']
    users.objects.filter(user_name=username).update(time_schedule=time_data)
    return HttpResponse('1')


def previous_activities(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    user_activity = users.objects.get(user_name=username).activities.split(',')
    pre_activity = []
    for activity in user_activity:
        try:
            _activity = activities.objects.get(name=activity, status=0).name
        except:
            pass
        else:
            pre_activity.append(_activity)

    activity_info = []
    for i in pre_activity:
        activity_time = str(activities.objects.get(name=i).time.date())
        activity_info.append((i, activity_time))
    return HttpResponse(json.dumps(activity_info), content_type='application/json')


def create_team(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    team_name = json_dic['team_name']
    team_introduction = json_dic['team_introduction']
    teams.objects.create(team_name=team_name,
                         team_introduction=team_introduction,
                         creator=username,
                         team_members=username)
    whether_upload = False
    if users.objects.get(user_name=username).time_schedule:
        whether_upload = True
    if whether_upload:
        teams.objects.filter(team_name=team_name).update(uploaded_person_number='1')

    user_team = users.objects.get(user_name=username).teams.split(',')
    user_team = list(user_team)
    user_team.append(team_name)
    new_user_teams = ''
    for i in range(len(user_team)):
        if i != 0:
            new_user_teams += ',' + user_team[i]
        if i == 0:
            new_user_teams += user_team[i]
    users.objects.filter(user_name=username).update(teams=new_user_teams)

    new_nickname = nickname.objects.create(user_name=username,
                                          team=team_name,
                                          nick_name=username)
    new_nickname.save()
    return HttpResponse('1')


def user(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    user_gender = users.objects.get(user_name=username).sex
    user_introduction = users.objects.get(user_name=username).self_introduction
    whether_upload = False
    if users.objects.get(user_name=username).time_schedule:
        whether_upload = True
    dic = {
        'user_gender': user_gender,
        'user_introduction': user_introduction,
        'whether_upload': whether_upload
    }
    return HttpResponse(json.dumps(dic), content_type='application/json')

def nickname_user(request):
    json_dic = eval(request.body)
    nick_name = json_dic['username']
    username = nickname.objects.get(nick_name=nick_name).user_name
    user_gender = users.objects.get(user_name=username).sex
    user_introduction = users.objects.get(user_name=username).self_introduction
    whether_upload = False
    if users.objects.get(user_name=username).time_schedule:
        whether_upload = True
    dic = {
        'user_gender': user_gender,
        'user_introduction': user_introduction,
        'whether_upload': whether_upload,
        'username': username
    }
    return HttpResponse(json.dumps(dic), content_type='application/json')


def team_info(request):
    json_dic = eval(request.body)
    team_name = json_dic['team_name']
    team_members = teams.objects.get(team_name=team_name).team_members.split(',')
    creator_name = teams.objects.get(team_name=team_name).creator
    creator_nick =  nickname.objects.get(user_name=creator_name, team=team_name).nick_name
    creator = [creator_name, creator_nick]
    introduction = teams.objects.get(team_name=team_name).team_introduction
    activities = []
    pre_activities = []
    try:
        activities = teams.objects.get(team_name=team_name).activities.split(',')
    except:
        pass
    try:
        pre_activities = teams.objects.get(team_name=team_name).previous_activities.split(',')
    except:
        pass
    up_loaded_persons = []
    for member in team_members:
        person = ''
        try:
            person = users.objects.get(user_name=member).time_schedule
        except:
            pass
        if person:
            up_loaded_persons.append(person)
    up_loaded = len(up_loaded_persons)

    nicknames = []
    for i in team_members:
        nick_name = nickname.objects.get(user_name=i, team=team_name).nick_name
        if nick_name:
            nicknames.append(nick_name)

    team_info = {
        'team_name': team_name,
        'team_members': team_members,
        'creator': creator,
        'introduction': introduction,
        'activities': activities,
        'pre_activities': pre_activities,
        'up_loaded': up_loaded,
        'nick_names': nicknames
    }
    return HttpResponse(json.dumps(team_info), content_type='application/json')

def get_results(team_name):
    team_members = teams.objects.get(team_name=team_name).team_members.split(",")
    time_schedules = []
    for member in team_members:
        time_schedule = users.objects.get(user_name=member).time_schedule
        time_schedules.append(time_schedule)

    for i in range(len(time_schedules)):
        if time_schedules[i] == None:
            time_schedules.remove(time_schedules[i])
    for i in range(len(time_schedules)):
        time_schedules[i] = list(time_schedules[i])
    percents = []
    for j in range(len(time_schedules[0])):
        times = []
        for i in range(len(time_schedules)):
            times += time_schedules[i][j]
        available = 0
        for h in times:
            if h == "1":
                available += 1
        percent = available / len(times)
        percents.append(percent)

        x = []
        for i in range(7):
            for j in range(12):
                x.append(j)
        y = []
        for i in range(12):
            for j in range(7):
                y.append(i)

    return x, y, percents


def results(request):
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
    import base64

    json_dic = eval(request.body)
    team_name = json_dic['team_name']

    x, y, z = get_results(team_name)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)


    matplotlib.rc('font', family='MicroSoft YaHei', weight='bold', size='12')
    plt.figure(figsize=(60, 40), dpi=80)
    ax = plt.subplot(projection='3d')
    # x = np.array(["周一","周二","周三","周四","周五","周六","周日"], dtype='string')
    # y = np.array([
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15",
    #     "8:30 ~ 9:15"
    # ], dtype='string')

    ax.bar3d(
        x,
        y,
        np.zeros_like(z),
        dx=0.1,
        dy=0.1,
        dz=z,
        color='red'
    )
    ax.set_zlabel('推荐指数')
    ax.set_ylabel('时间段')
    ax.set_xlabel('日期')
    # plt.title('分析结果')
    plt.savefig('media/result.jpg')

    try:
        with open('media/result.jpg', 'rb') as f:
            image_data = base64.b64encode(f.read())
        return HttpResponse(image_data, content_type="image/jpg")
    except Exception as e:
        print(e)
        return HttpResponse(str(e))

def results2(request):
    json_dic = eval(request.body)
    team_name = json_dic['team_name']

    x, y, z = get_results(team_name)
    li = []
    for i in range(len(x)):
        li.append([z[i], x[i], y[i]])
    li = sorted(li,key=(lambda x:x[0]),reverse=True)
    li = li[:10]
    for i in li:
        i[0] = str(i[0]*100)+"%"
        if i[2] == 0:
            i[2] = "一"
        elif i[2] == 1:
            i[2] = "二"
        elif i[2] == 2:
            i[2] = "三"
        elif i[2] == 3:
            i[2] = "四"
        elif i[2] == 4:
            i[2] = "五"
        elif i[2] == 5:
            i[2] = "六"
        elif i[2] == 6:
            i[2] = "日"
        if i[1] == 0:
            i[1] = "8:30 ~ 9:15"
        elif i[1] == 1:
            i[1] = "9:25 ~ 10:10"
        elif i[1] == 2:
            i[1] = "10:30 ~ 11:15"
        elif i[1] == 3:
            i[1] = "11:25 ~ 12:10"
        elif i[1] == 4:
            i[1] = "14:30 ~ 15:15"
        elif i[1] == 5:
            i[1] = "15:25 ~ 16:10"
        elif i[1] == 6:
            i[1] = "16:30 ~ 17:15"
        elif i[1] == 7:
            i[1] = "17:25 ~ 18:10"
        elif i[1] == 8:
            i[1] = "19:00 ~ 19:45"
        elif i[1] == 9:
            i[1] = "19:55 ~ 20:40"
        elif i[1] == 10:
            i[1] = "20:50 ~ 21:35"
        elif i[1] == 11:
            i[1] = "21:45 ~ 22:30"

    return HttpResponse(json.dumps(li), content_type='application/json')


def leave_team(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    team_name = json_dic['team_name']

    user_teams = users.objects.get(user_name=username).teams.split(',')
    new_user_teams = ''
    for i in range(len(user_teams)):
        if user_teams[i] == team_name:
            user_teams.remove(user_teams[i])
            break
    for i in range(len(user_teams)):
        if i != 0:
            new_user_teams += ',' + user_teams[i]
        if i == 0:
            new_user_teams += user_teams[i]
    users.objects.filter(user_name=username).update(teams=new_user_teams)

    team_members = teams.objects.get(team_name=team_name).team_members.split(',')
    new_team_members = ''
    for i in range(len(team_members)):
        if team_members[i] == username:
            team_members.remove(team_members[i])
    for i in range(len(team_members)):
        if i != 0:
            new_team_members += ',' + team_members[i]
        if i == 0:
            new_team_members += team_members[i]
    teams.objects.filter(team_name=team_name).update(team_members=new_team_members)

    nickname.objects.filter(user_name=username).delete()
    return HttpResponse('1')


def change_team_name(request):
    json_dic = eval(request.body)
    team_name = json_dic['team_name']
    new_team_name = json_dic['new_team_name']

    teams.objects.filter(team_name=team_name).update(team_name=new_team_name)

    team_members = teams.objects.get(team_name=new_team_name).team_members.split(',')
    for team_member in team_members:
        member_teams = users.objects.get(user_name=team_member).teams.split(',')
        new_user_teams = ''
        for i in range(len(member_teams)):
            if member_teams[i] == team_name:
                member_teams[i] = new_team_name
            if i != 0:
                new_user_teams += ',' + member_teams[i]
            elif i == 0:
                new_user_teams += member_teams[i]
        users.objects.filter(user_name=team_member).update(teams=new_user_teams)

    team_activities = ''
    try:
        team_activities = teams.objects.get(team_name=new_team_name).activities.split(',')
    except:
        pass
    if team_activities:
        for team_activitiy in team_activities:
            activities.objects.filter(name=team_activitiy).update(team=new_team_name)

    pre_team_activities = ''
    try:
        pre_team_activities = teams.objects.get(team_name=new_team_name).previous_activities.split(',')
    except:
        pass
    if pre_team_activities:
        for pre_team_activitiy in pre_team_activities:
            activities.objects.filter(name=pre_team_activitiy).update(team=new_team_name)

    return HttpResponse('1')


def change_team_introduction(request):
    json_dic = eval(request.body)
    team_name = json_dic['team_name']
    new_team_introduction = json_dic['new_team_introduction']
    try:
        teams.objects.filter(team_name=team_name).update(team_introduction=new_team_introduction)
        return HttpResponse('1')
    except:
        return HttpResponse('0')


def check_activity_in_team(request):
    import datetime
    json_dic = eval(request.body)
    team_name = json_dic['team_name']
    activity_names = []
    pre_activity_names = []
    try:
        activity_names = teams.objects.get(team_name=team_name).activities.split(',')
    except:
        pass
    try:
        pre_activity_names = teams.objects.get(team_name=team_name).previous_activities.split(',')
    except:
        pass
    activities_dic = [[], []]
    if activity_names:
        for i in activity_names:
            if i:
                activity = activities.objects.get(name=i)
                activity_dic = {'name': i,
                                'time': str(activity.time.date()), }
                activities_dic[0].append(activity_dic)
    if pre_activity_names:
        for i in pre_activity_names:
            if i:
                activity = activities.objects.get(name=i)
                activity_dic = {'name': activity_name,
                                'time': str(activity.time.date()), }
                activities_dic[1].append(activity_dic)
    return HttpResponse(json.dumps(activities_dic), content_type='application/json')


def dismiss_team(request):
    json_dic = eval(request.body)
    team_name = json_dic['team_name']

    team_members = teams.objects.get(team_name=team_name).team_members.split(',')
    team_activities = ''
    team_pre_activities = ''
    try:
        team_activities = teams.objects.get(team_name=team_name).activities.split(',')
    except:
        pass
    try:
        team_pre_activities = teams.objects.get(team_name=team_name).previous_activities.split(',')
    except:
        pass
    totel_activities = team_activities + team_pre_activities
    teams.objects.filter(team_name=team_name).delete()

    for username in team_members:
        user_teams = users.objects.get(user_name=username).teams.split(',')
        new_user_teams = ''
        for i in range(len(user_teams)):
            if user_teams[i] == team_name:
                user_teams.remove(user_teams[i])
                break
        for i in range(len(user_teams)):
            if i != 0:
                new_user_teams += ',' + user_teams[i]
            if i == 0:
                new_user_teams += user_teams[i]
        users.objects.filter(user_name=username).update(teams=new_user_teams)

        new_user_activity = ''
        for delete_activity in totel_activities:
            user_activities = users.objects.get(user_name=username).activities.split(',')
            for i in range(len(user_activities)):
                if delete_activity == user_activities[i]:
                    user_activities.remove(user_activities[i])
                else:
                    if i != 0:
                        new_user_activity += ',' + user_activities[i]
                    if i == 0:
                        new_user_activity += user_activities[i]
            users.objects.filter(user_name=username).update(activities=new_user_activity)

    if totel_activities:
        for activity in totel_activities:
            activities.objects.filter(name=activity).delete()

    for username in team_members:
        nickname.objects.filter(user_name=username, team=team_name).delete()

    return HttpResponse('1')


def search_for_activity(request):
    import datetime
    json_dic = eval(request.body)
    activity_name = json_dic['activity_name']

    result = []
    activities_list = activities.objects.filter(team__isnull=True)
    for activity in activities_list:
        if activity_name in activity.name:
            activity = activities.objects.get(name=activity.name)
            dic = {
                'name': activity.name,
                'launcher': activity.launcher,
                'time': str(activity.time.date()),
                'location': activity.location
            }
            result.append(dic)
    return HttpResponse(json.dumps(result), content_type='application/json')

def sign_in_activity(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    activity = json_dic['activity']

    user_activities = []
    try:
        user_activities = users.objects.get(user_name=username).activities.split(',')
    except:
        pass
    if activity in user_activities:
        return HttpResponse('have_been_in')
    else:
        user_activities.append(activity)
        new_user_activity = ''
        for i in range(len(user_activities)):
            if i != 0:
                new_user_activity += ',' + user_activities[i]
            if i == 0:
                new_user_activity += user_activities[i]
        users.objects.filter(user_name=username).update(activities=new_user_activity)

        activity_participants = activities.objects.get(name=activity).participants.split(',')
        new_activity_participants = ''
        activity_participants.append(username)
        for j in range(len(activity_participants)):
            if j != 0:
                new_activity_participants += ',' + activity_participants[j]
            if j == 0:
                new_activity_participants += activity_participants[j]
        activities.objects.filter(name=activity).update(participants=new_activity_participants)
        return HttpResponse('sign_in')


def delete_activity(request):
    json_dic = eval(request.body)
    activity = json_dic['activity']
    paricipants = activities.objects.get(name=activity).participants.split(',')

    try:
        activity_team = activities.objects.get(name=activity).team
    except:
        pass
    else:
        team_activity = []
        try:
            team_activity = teams.objects.get(team_name=activity_team).activities.split(',')
        except:
            pass
        if team_activity:
            for i in range(len(team_activity)):
                if team_activity[i] == activity:
                    team_activity.remove(team_activity[i])
                    break

        team_pre_activity = []
        try:
            team_pre_activity = teams.objects.get(team_name=activity_team).previous_activities.split(',')
        except:
            pass
        if team_pre_activity:
            for i in range(len(team_pre_activity)):
                if team_pre_activity[i] == activity:
                    team_pre_activity.remove(team_pre_activity[i])
                    break

        new_team_activities = ''
        for j in range(len(team_activity)):
            if j != 0:
                new_team_activities += ',' + team_activity[j]
            if j == 0:
                new_team_activities += team_activity[j]
        teams.objects.filter(team_name=activity_team).update(activities=new_team_activities)

        new_team_activities = ''
        for j in range(len(team_pre_activity)):
            if j != 0:
                new_team_activities += ',' + team_pre_activity[j]
            if j == 0:
                new_team_activities += team_pre_activity[j]
        teams.objects.filter(team_name=activity_team).update(previous_activities=new_team_activities)

    for i in paricipants:
        user_activities = users.objects.get(user_name=i).activities.split(',')
        for j in user_activities:
            if j == activity:
                user_activities.remove(j)
                break
        new_activities = ''
        for j in range(len(user_activities)):
            if j != 0:
                new_activities += ',' + user_activities[j]
            if j == 0:
                new_activities += user_activities[j]
        users.objects.filter(user_name=i).update(activities=new_activities)

    activities.objects.get(name=activity).delete()
    return HttpResponse('deleted')

def show_people_in_activity(request):
    json_dic = eval(request.body)
    activity = json_dic['activity']
    participants = activities.objects.get(name=activity).participants.split(',')
    return HttpResponse(json.dumps(participants), content_type='application/json')


def search_for_users(request):
    json_dic = eval(request.body)
    user = json_dic['user']
    all_users = users.objects.values_list('user_name')
    results = []
    for user_name in all_users:
        if user in user_name[0]:
            results.append(user_name[0])
    if results:
        return HttpResponse(json.dumps(results), content_type='application/json')
    else:
        return HttpResponse('No')


def add_member(request):
    json_dic = eval(request.body)
    user = json_dic['user']
    team = json_dic['team']

    team_members = teams.objects.get(team_name=team).team_members.split(',')
    team_members.append(user)
    new_team_members = ''
    for i in range(len(team_members)):
        if i != 0:
            new_team_members += ',' + team_members[i]
        if i == 0:
            new_team_members += team_members[i]
    teams.objects.filter(team_name=team).update(team_members=new_team_members)

    user_team =[]
    try:
        user_team = users.objects.get(user_name=user).teams.split(',')
    except:
        pass
    user_team = list(user_team)
    for i in user_team:
        if not i:
            user_team.remove(i)
    user_team.append(team)
    new_user_teams = ''
    for i in range(len(user_team)):
        if i != 0:
            new_user_teams += ',' + user_team[i]
        if i == 0:
            new_user_teams += user_team[i]
    users.objects.filter(user_name=user).update(teams=new_user_teams)

    new_nickname = nickname.objects.create(user_name=user,
                                          team=team,
                                          nick_name=user)
    new_nickname.save()
    return HttpResponse('1')


def delete_member(request):
    json_dic = eval(request.body)
    user = json_dic['user']
    team = json_dic['team']

    team_members = teams.objects.get(team_name=team).team_members.split(',')
    for i in team_members:
        if i == user:
            team_members.remove(i)
    new_team_members = ''
    for i in range(len(team_members)):
        if i != 0:
            new_team_members += ',' + team_members[i]
        if i == 0:
            new_team_members += team_members[i]
    teams.objects.filter(team_name=team).update(team_members=new_team_members)

    user_team = users.objects.get(user_name=user).teams.split(',')
    user_team = list(user_team)
    for i in user_team:
        if not i:
            user_team.remove(i)
        if i == team:
            user_team.remove(i)
    new_user_teams = ''
    for i in range(len(user_team)):
        if i != 0:
            new_user_teams += ',' + user_team[i]
        if i == 0:
            new_user_teams += user_team[i]
    users.objects.filter(user_name=user).update(teams=new_user_teams)

    nickname.objects.filter(user_name=user).delete()
    return HttpResponse('1')

def check_friends(request):
    json_dic = eval(request.body)
    username = json_dic['user']
    members = []
    try:
        members = json_dic['members']
    except:
        pass
    try:
        friends = users.objects.get(user_name=username).friends.split(',')
        if members:
            for i in friends:
                for j in members:
                    if i == j:
                        friends.remove(i)
        return HttpResponse(json.dumps(friends), content_type='application/json')
    except:
        return HttpResponse('No')

def check_team_members(request):
    json_dic = eval(request.body)
    team = json_dic['team']
    username = json_dic['username']
    team_members = teams.objects.get(team_name=team).team_members.split(',')
    team_members_nick = []
    for member in team_members:
        if member == username:
            team_members.remove(member)
    for member in team_members:
        nick_name = nickname.objects.get(team=team, user_name=member).nick_name
        team_members_nick.append(nick_name)
    return HttpResponse(json.dumps(team_members_nick), content_type='application/json')


def check_team_upload(request):
    json_dic = eval(request.body)
    team_name = json_dic['team_name']

    team_members = teams.objects.get(team_name=team_name).team_members.split(',')
    dic = {}
    for i in team_members:
        whether_upload = ''
        try:
            whether_upload = users.objects.get(user_name=i).time_schedule
        except:
            pass
        if whether_upload:
            dic.update({i: '1'})
        if not whether_upload:
            dic.update({i: '0'})
    return HttpResponse(json.dumps(dic), content_type='application/json')

def change_nickname(request):
    json_dic = eval(request.body)
    user_name = json_dic['user_name']
    team = json_dic['team_name']
    nick_name = json_dic['nick_name']

    nickname.objects.filter(team=team, user_name=user_name).update(nick_name=nick_name)
    return HttpResponse('1')



def send_verify(request):
    json_dic = eval(request.body)
    user_name = json_dic['user_name']
    to_add_name = json_dic['username']
    verify_message = json_dic['verify_message']

    to_adds = users.objects.get(user_name=to_add_name).to_add_friends.split(',')
    for i in to_adds:
        if not i:
            to_adds.remove(i)
    item = str(user_name)+";"+str(verify_message)
    to_adds.append(item)
    new_to_adds = ''
    for j in range(len(to_adds)):
        if j != 0:
            new_to_adds += ',' + to_adds[j]
        if j == 0:
            new_to_adds += to_adds[j]
    users.objects.filter(user_name=to_add_name).update(to_add_friends=new_to_adds)

    return HttpResponse('ok')


def response(request):
    json_dic = eval(request.body)
    user_name = json_dic['user']
    target_user = json_dic['target_user']
    choice = json_dic['choice']

    to_adds = users.objects.get(user_name=user_name).to_add_friends.split(',')
    for i in to_adds:
        if not i:
            to_adds.remove(i)
    for i in to_adds:
        item = i.split(';')
        if item[0] == target_user:
            to_adds.remove(i)
            break
    new_to_adds = ''
    for j in range(len(to_adds)):
        if j != 0:
            new_to_adds += ',' + to_adds[j]
        if j == 0:
            new_to_adds += to_adds[j]
    users.objects.filter(user_name=user_name).update(to_add_friends=new_to_adds)

    if choice == 'consent':
        friends1 = []
        try:
            friends1 = users.objects.get(user_name=user_name).friends.split(',')
        except:
            pass
        friends1.append(target_user)
        new_friends1 = ''
        for j in range(len(friends1)):
            if j != 0:
                new_friends1 += ',' + friends1[j]
            if j == 0:
                new_friends1 += friends1[j]
        users.objects.filter(user_name=user_name).update(friends=new_friends1)

        friends2 = []
        try:
            friends2 = users.objects.get(user_name=target_user).friends.split(',')
        except:
            pass
        friends2.append(user_name)
        new_friends2 = ''
        for j in range(len(friends2)):
            if j != 0:
                new_friends2 += ',' + friends2[j]
            if j == 0:
                new_friends2 += friends2[j]
        users.objects.filter(user_name=target_user).update(friends=new_friends2)

    return HttpResponse('ok')


def search_team(request):
    json_dic = eval(request.body)
    team_name = json_dic['team_name']

    result = []
    team_list = teams.objects.filter()
    for team in team_list:
        if team_name in team.team_name:
            team = teams.objects.get(team_name=team.team_name)
            dic = {
                'name': team.team_name,
                'member_num': len(team.team_members.split(','))
            }
            result.append(dic)

    return HttpResponse(json.dumps(result), content_type='application/json')
