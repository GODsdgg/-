from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from users.models import User
# from apps.users.models import User    错误的

# apps.users  我们已经告诉系统 users 在哪里了,就不需要添加 apps

"""
一. 确定需求
二.确定采用那种请求方式 和 url
三.实现


1.前段发送一个ajax请求给后端,参数是 用户名

2.后端接受用户名
3.查询校验是否重复
4.返回响应

GET           /users/usernames/(?P<username>\w{5,20})/count/


"""
#APIView
# GenericAPIView            列表,详情通用支持,一般和mixin配合使用
# ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
"""
1.前段传递过来的数据 已经在 url中校验过了
2.我们也不需要 序列化器
"""
class RegisterUsernameCountView(APIView):

    def get(self,request,username):
        #2.后端接受用户名
        # username
        #3.查询校验是否重复
        #count = 0 表示没有注册
        #count = 1 表示注册
        count = User.objects.filter(username=username).count()

        #4.返回响应
        return Response({'count':count,'username':username})

class RegisterPhoneCountAPIView(APIView):
    """
    查询手机号的个数
    GET: /users/phones/(?P<mobile>1[345789]\d{9})/count/
    """
    def get(self,request,mobile):

        #通过模型查询获取手机号个数
        count = User.objects.filter(mobile=mobile).count()
        #组织数据
        context = {
            'count':count,
            'mobile':mobile
        }

        return Response(context)



"""
前端应该将 6个参数(username,password,password2,mobile,sms_code,allow) 传递给后端

1.接收前端提交的数据
2.校验数据
3.数据入库
4.返回响应

POST            users/

"""
#APIView
# GenericAPIView            列表,详情通用支持,一般和mixin配合使用
# ListAPIView,RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import CreateAPIView
from .serializers import RegisterCreateUserSeaializer
from rest_framework_jwt.utils import jwt_response_payload_handler
class RegisterCreateUserView(APIView):

    def post(self,request):
        # 1.接收前端提交的数据
        # username = request.form.get('username')
        # username = request.form.get('username')
        # username = request.form.get('username')
        data = request.data
        # 2.校验数据
        # if not all([]):
        #     pass
        serializer = RegisterCreateUserSeaializer(data=data)

        serializer.is_valid(raise_exception=True)
        # 3.数据入库
        serializer.save()
        # 4.返回响应
        # user -  序列化器->  字典
        # serializer.data --- 将模型转换为字典的过程
        # 序列化器的 序列化(模型-->字典)操作原理是:
        # 我们的序列化器 根据 字段来获取 模型的属性的值,来转换为字典

        return Response(serializer.data)

"""

一.断点
 	    在程序的入口出
 	    部分代码实现一个功能
 	    认为哪里有错误
 	    每行都加

二.事件的触发点
 	    很好的确定代码写在哪里

用户注册之后,直接跳转到首页,默认表示已经登录

#注册完成应该 返回给客户端一个token
#1.如何生成token
#2.在哪里返回

"""

#APIView
# GenericAPIView            列表,详情通用支持,一般和mixin配合使用
# ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCenterSerializer
# class UserCenterView(APIView):
#
#     """
#     登录用户访问个人中心的时候 ,我们需要将个人信息返回获取
#
#     1. 如何确定是登录用户  --> 需要前端传递一个token过来
#     2. 获取用户信息
#     3. 返回数据
#
#     GET     /users/infos/
#     """
#     # 权限
#     # 1.登录用户访问权限
#     permission_classes = [IsAuthenticated]
#
#     def get(self,request):
#         # 2.获取用户信息
#         user = request.user
#         # 3.返回数据
#         serializer = UserCenterSerializer(user)
#         return Response(serializer.data)



from rest_framework.mixins import RetrieveModelMixin

from rest_framework.generics import RetrieveAPIView

class UserCenterView(RetrieveAPIView):

    serializer_class = UserCenterSerializer

    queryset = User.objects.all()
    # 权限
    permission_classes = [IsAuthenticated]

    def get_object(self):

        # 获取某一个指定的对象
        return self.request.user