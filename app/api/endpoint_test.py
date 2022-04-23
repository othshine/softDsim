from django.db import models
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import serializers, status


class Test(models.Model):
    req = models.CharField("req", max_length=5)
    msg = models.CharField("msg", max_length=200)

    @classmethod
    def create(cls, req, msg):
        test = cls(req=req, msg=msg)
        return test
    
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test 
        fields = ('req', 'msg')


@api_view(['GET', 'POST'])
def api_test(request):
    if request.method == 'GET':
        t = Test.create("GET", "Hi from Django")
        serializer = TestSerializer(t ,context={'request': request}, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        t = Test.create("POST", "Hi from Django")
        serializer = TestSerializer(t ,context={'request': request}, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

