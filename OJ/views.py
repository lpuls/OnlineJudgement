from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse
from django import template, forms
import time

from Codes.DataBase import DataBaseLinker

def hi(request):
    if 'userName' in request.POST and 'passWord' in request.POST:
        userName = str(request.POST['userName'])
        passWord = str(request.POST['passWord'])
        data = DataBaseLinker.getInstance().execute("select * from Users where user_id='" + userName + "' and user_password='" + passWord + "'")
        request.session['userName'] = userName
        print data
        if len(data):
            return HttpResponse("Please receive my warm welcome")
    return HttpResponse("Get Out")

def upload(request):
    if 'codes' in request.POST and 'type' in request.POST:
        codes = str(request.POST['codes'])
        tp = request.POST['type']
        userName = request.session['userName']
        questionID = request.session['ID']
        nowTime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        filePath = '/home/xp/TempCodes/' + userName + '_' + str(nowTime) + '.' + tp
        code = file(filePath,'w');
        code.write(codes)
        return HttpResponse(codes + '   ' + tp)
    return HttpResponse('None')

def questions(request):
    file = open("media/questions.html")
    t = template.Template(file.read())
    file.close()
    html = t.render(template.Context({'question':'/question/0000'}))
    return HttpResponse(html)

