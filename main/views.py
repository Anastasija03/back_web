from os import access, name
from django.shortcuts import redirect, render
from django.views.generic import View
from .models import *

from django.db.models import Q

from rest_framework import views
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import serializers
from rest_framework import filters
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet

import django_filters.rest_framework

""" Serializers """

####################################################

class UserFormSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    years = serializers.IntegerField()
    email = serializers.EmailField()
    country = serializers.CharField()

####################################################



""" API views для Инженерки """

####################################################

@api_view(["POST"]) # POST и свой serializer
def APICreateUserForm(request):
    if request.method == 'POST':
        serializer = UserFormSerializer(data=request.data)

        if serializer.is_valid():
            UserForm.objects.create(
                name=request.data['name'],
                surname=request.data['surname'],
                years=request.data['years'],
                email=request.data['email'],
                country=request.data['country'],
            )

            return Response({}, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class APIGetUserForms(ModelViewSet): # SEARCHFILTER
    queryset = UserForm.objects.all()
    serializer_class = UserFormSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'country']


class APIGetUserFormsParams(ModelViewSet): # Фильтр по GET параметрам и Q()
    serializer_class = UserFormSerializer
    queryset = UserForm.objects.all()

    def get_queryset(self): # Переписываем стандартный метод чтобы фильтровать по GET параметрам
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')

        if email:
            queryset = UserForm.objects.filter(Q(name=name) & Q(email=email))
        else:
            queryset = UserForm.objects.filter(Q(name=name))

        return queryset
    

class APIGetUserFormsDJFilters(ModelViewSet): # DJANGO_FILTERS
    serializer_class = UserFormSerializer
    queryset = UserForm.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'email', 'country']


#######################################################

""" Обычные views """

class Index(View):
    def get(self, request):
        return render(request, 'index.html')

class QuizPage(View):
    def get(self, request, pk, quest):

        try:
            context= {
            "question": Quiz.objects.get(pk=pk).questions.all()[int(quest)],
            "next": int(quest) + 1,
            "quiz": pk,
            "count": len(Quiz.objects.get(pk=pk).questions.all())
            }
        except:
            return redirect("quiz_list")

        return render(request, 'quiz.html', context=context)

class QuizList(View):
    def get(self, request):

        context = {"list": Quiz.objects.all()}

        return render(request, 'quiz_list.html', context=context)


class FormPage(View):
    def get(self, request):
        return render(request, 'form.html')

    def post(self, request):

        newUser = UserForm.objects.create(
            name=request.POST['name'],
            surname=request.POST['surname'],
            years=request.POST['years'],
            email=request.POST['email'],
            country=request.POST['country'],
        )
        return redirect("index")


class ProposePage(View):
    def get(self, request):
        return render(request, 'propose.html')

    def post(self, request):

        newPropose = ProposeForm.objects.create(
            title=request.POST['title'],
            topic=request.POST['topic'],
            description=request.POST['description']
        )

        return redirect("index")