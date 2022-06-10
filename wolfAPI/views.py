import pandas as pandas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Role, GameParameters, Player
from django.contrib.auth.models import User
from .serializers import RoleSerializer, GameParametersSerializer, PlayerSerializer

import json


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.first_name
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RoleList(generics.ListAPIView):
    serializer_class = RoleSerializer

    def get_queryset(self):
        user = self.kwargs['pk']
        return Role.objects.filter(user__id=user)


@api_view(('GET',))
@renderer_classes((JSONRenderer,))
def main(request, pk):
    if not Role.objects.filter(user__id=pk):
        df = pandas.read_csv('basicroles.csv')
        for index, row in df.iterrows():
            row = Role(
                score=row['role_score'],
                title=row['role_title'],
                description=row['role_description'],
                alignment=row['role_alignment'],
                type=row['role_type'],
                user=request.user
            )
            row.save()
    if not GameParameters.objects.filter(user__id=pk):
        j = {key: True for key in
             Role.objects.filter(user__id=pk).order_by().values_list('type', flat=True).distinct()}

        preferences = GameParameters(typePreferences=json.dumps(j), wolfCount=2, balanceGoal=0, playerCount=7, user=User.objects.get(id=pk))
        preferences.save()
    roles = Role.objects.filter(user__id=pk)
    gameParameters = GameParameters.objects.get(user__id=pk)
    players = Player.objects.filter(user__id=pk)
    roleSerializer = RoleSerializer(roles, many=True)
    parameterSerializer = GameParametersSerializer(gameParameters, many=False)
    playerSerializer = PlayerSerializer(players, many=True)
    return Response({'roles': roleSerializer.data, 'parameters': parameterSerializer.data, 'players': playerSerializer.data})


def rollChange(request):
    body = json.loads(request.body.decode('utf-8'))
    Player.objects.filter(user__id=body['user']['user_id']).delete()
    if request.method == "POST":
        print(body['roleTypes'])
        for player in body['players']:
            newPlayer = Player(name=player, user=User.objects.get(id=body['user']['user_id']))
            newPlayer.save()
        GameParameters.objects.filter(user__id=body['user']['user_id']).update(typePreferences=json.dumps(body['roleTypes']))
    return HttpResponse(201)
