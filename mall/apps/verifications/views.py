from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

"""
一. 先把需求写下来(因为写下来很清晰,而且 一些东西不会遗忘)
二. 根据需要  确定 采用那种请求方
三. 确定视图 进行编码

1. 前端需要发送给我一个  uuid  这个时候 我们接受到uuid之后生成一张图片,给前端


2.接受前端的uuid
3.生成图片验证码,保存 图片验证码的数据
4.返回响应

GET                 /verifications/imagecodes/(?P<image_code_id>.+)/

"""
#APIView
# GenericAPIView            列表,详情通用支持,一般和mixin配合使用
# ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
class RegisterImageCodeView(APIView):
    """
    # 2.接受前端的uuid
    # 3.生成图片验证码,保存 图片验证码的数据
    # 4.返回响应
    """
    def get(self,request,image_code_id):
        # 2.接受前端的uuid
        text,image = captcha.generate_captcha()

        # 3.生成图片验证码,保存redis 图片验证码的数据
        redis_conn = get_redis_connection('code')
        from . import constant
        redis_conn.setex('img_%s'%image_code_id,constant.IMAGE_CODE_EXPIRE_TIME,text)
        # 4.返回响应
        return HttpResponse(image,content_type='image/jpeg')

"""
当用户点击 获取短信验证码的时候,前端应该将 手机号,图片验证码和uuid(image_code_id) 发送给后端

1.接受前端数据
2.校验数据
3.先生成短信验证码
4.发送短信
5.返回响应

GET           /verifications/sms_codes/mobile/uuid/text
GET           /verifications/sms_codes/?mobile=xxxx&uuid=xxx&text=xxx
GET          /verifications/sms_codes/?P<mobil>1[3-9]\d{9}/?uuid=xxx&text=xxx      选这个

"""
#APIView
# GenericAPIView            列表,详情通用支持,一般和mixin配合使用
# ListAPIView,RetrieveAPIView
from . serializers import RegisterSmscodeSerializer
from libs.yuntongxun.sms import CCP
class RegisterSmscodeView(APIView):

    def get(self,request,mobile):
        # 1.接受前端数据
        params = request.query_params
        # 2.校验数据 --- 放到了序列化器中
        # text = params.get('text')
        # image_code_id = params.get('dd')
        #
        # if not all(text,image_code_id):
        # 校验
        serializer = RegisterSmscodeSerializer(data=params)
        #  调用is_valid 才会校验
        serializer.is_valid(raise_exception=True)

        # 3.先生成短信验证码
        from random import randint
        sms_code = '%06d'%randint(0,999999)
        # 4.保存短信 发送短信
        redis_conn = get_redis_connection('code')
        redis_conn.setex('sms_%s'%mobile,300,sms_code)

        CCP().send_template_sms(mobile,[sms_code,5],1)

        # 5.返回响应
        return Response({'msg':'ok'})

