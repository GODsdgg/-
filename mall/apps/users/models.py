from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


"""
1.采用Flask方式,完全自定义
2.采用django自带的用户模型,模型中缺少一个手机号字段


"""

class User(AbstractUser):

    """
    用户模型类
    """

    mobile = models.CharField(max_length=11,unique=True,verbose_name='手机号')

    email_active = models.BooleanField(default=False,verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
