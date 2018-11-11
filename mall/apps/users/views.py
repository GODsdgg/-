from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response


from users.models import User
# from apps.users.models import User    错误的
from users.utlis import generic_active_url, get_active_user

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



"""
用户在点击设置的时候,输入 邮箱信息, 当点击保存的时候 需要将邮箱信息发送给后端


1. 这个接口必须是登录才可以访问
2. 接收参数
3. 验证数据
4. 更新数据
5. 发送激活邮件
6. 返回响应

PUT         /users/emails/
"""
# APIView
# GenericAPIView                    列表,详情通用支持,一般和mixin配合使用
# UpdateAPIView
from .serializers import UserEmailSerializer
from rest_framework.mixins import UpdateModelMixin
from django.conf import settings

class UserEmailView(APIView):

    # 1. 这个接口必须是登录才可以访问
    permission_classes = [IsAuthenticated]

    def put(self,request):
        # 2. 接收参数
        data = request.data
        # 3. 验证数据
        user = request.user
        serializer = UserEmailSerializer(instance=user,data=data)
        serializer.is_valid(raise_exception=True)
        # 4. 更新数据
        serializer.save()


        # Celery 可以理解为一个消息中心

        from celery_tasks.email.tasks import send_active_email

        send_active_email.delay(data.get('email'),request.user.id)
        # # 5. 发送激活邮件
        # from django.core.mail import send_mail
        # # subject, message, from_email, recipient_list,
        # # subject, 主题
        # subject = '美多商城激活邮件'
        # # message,     内容
        # message = ''
        # # from_email,  发件人
        # from_email = settings.EMAIL_FROM
        # # recipient_list, 接收人列表
        # email = data.get('email')
        # recipient_list = [email]
        # # 可以设置以下 html的样式等信息
        # verify_url = generic_active_url(user.id, email)
        #
        # html_message = '<p>尊敬的用户您好！</p>' \
        #                  '<p>感谢您使用美多商城。</p>' \
        #                  '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
        #                  '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)
        #
        # send_mail(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list,
        #           html_message=html_message
        #           )
        # 6. 返回响应
        return Response(serializer.data)



# from rest_framework.generics import UpdateAPIView
# class UpdataEmailView(UpdateAPIView):
#
#     serializer_class = UserEmailSerializer
#
#     # queryset = User.objects.all()
#
#     def get_object(self):
#
#         return self.request.user


from rest_framework import status
class UserActiveEmailView(APIView):

    """
    当用户点击激活连接的时候,会跳转到一个页面,这个页面中含有 token(含有 用户id和email信息)信息
    前端需要发送一个ajax请求,将 token 发送给后端

    1. 接受token
    2. 对token进行解析
    3. 返回响应

    GET     /users/emails/verification/?token=xxx
    """
    def get(self,request):
        # 1.接受token
        token = request.query_params.get('token')
        if token is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # {id:xxx,email:xxx}
        # 2. 对token进行解析

        # id = xxx

        user = get_active_user(token)
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.email_active = True
        user.save()

        # 3.返回响应
        return Response({'msg':'ok'})