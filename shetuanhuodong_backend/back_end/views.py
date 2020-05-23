from django.shortcuts import render
# from django import HttpResponse
from django.http import HttpResponse
import MySQLdb

db = MySQLdb.connect(user="yang", db="back_end", password="yang", host="localhost")
cursor = db.cursor()

# Create your views here.
def login(request):
    json_dic = eval(request.body)
    username = json_dic['username']
    password = json_dic['password']
    cursor.execute('select user_name from back_end_users')
    dbusername = cursor.fetchall()[0][0]
    cursor.execute('select password from back_end_users')
    dbpassword = cursor.fetchall()[0][0]
    if username == dbusername and password == dbpassword:
        return HttpResponse("true")
    else:
        return HttpResponse("false")

def register(request):
    import datetime
    json_dic = eval(request.body)
    username = json_dic['username']
    password = json_dic['password']
    phone_number = json_dic['phone_number']
    create_time = datetime.datetime.now()
    try:
        cursor.execute("insert into back_end_users (user_name, password, create_time, phone_number)"
                       " values ('{0}','{1}', '{2}','{3}')".format(username, password,create_time, phone_number))
    except:
        return HttpResponse("false")
    else:
        return HttpResponse("true")



