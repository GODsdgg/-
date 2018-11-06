from rest_framework import serializers
from users.models import User
# serializers.ModelSerializer
# serializers.Serializer

# 数据入库  选择 ModelSerializer 肯定有 模型
class RegisterCreateUserSeaializer(serializers.ModelSerializer):

    """
    6个参数(username,password,password2,mobile,sms_code,allow)
    """

    sms_code = serializers.CharField(label='短信验证码',min_length=6,max_length=6,required=True)
    password2 = serializers.CharField(label='确认密码',required=True)
    allow = serializers.CharField(label='确认密码',required=True)
    # ModelSerializer 自动生成字段的时候 是根据 fields 列表生成的
    class Meta:
        model = User
        fields = ['username','password','mobile']

