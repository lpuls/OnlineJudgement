from django.db import models
from django import template

__author__ = 'xp'

from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse

def index(request):
    return render_to_response("index2.html")



def question(request, questionId):
        return render_to_response("question.html")

