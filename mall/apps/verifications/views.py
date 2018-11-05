from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

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



