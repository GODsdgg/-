from rest_framework import serializers
from .models import Area

#暂时理解为省的序列化器
class AreaSerailizer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ['id','name']



class AreaSubSerializer(serializers.ModelSerializer):

    # 这个是 市的序列化器

    subs = AreaSerailizer(many=True)

    class Meta:
        model = Area
        fields = ['id','name','subs']