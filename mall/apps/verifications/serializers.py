from rest_framework import serializers
from django_redis import get_redis_connection
# serializers.ModelSerializer
# serializers.Serializer

# 我们的数据没有模型,选择Serializer
class RegisterSmscodeSerializer(serializers.Serializer):

    test = serializers.CharField(label='图片验证码',min_length=4,max_length=4,required=True)
    # UUID
    image_code_id = serializers.UUIDField(label='uuid',required=True)

    """
    校验:
        1.字段类型
        2.字段选项
        3.单个字段
        4.多个字段

        校验图片验证码的时候 需要用到 text和 iamge_code_id 这2个字段,所以选择 多个字段校验
    """

    # def validate(self, data):
    def validate(self, attrs):

        # data --> attrs
        #1. 用户提交的图片验证码
        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')
        # 2. 获取redis验证码

        # 2.1连接redis
        redis_conn = get_redis_connection('code')

        # 2.2获取redis_text
        redis_text = redis_conn.get('img_%s'%image_code_id)

        # 2.3 判断是否过期
        if redis_text is None:
            raise serializers.ValidationError('图片验证码已过期')

        # 3.比对
        # 2个注意点:  redis_text 是bytes而理性
        #           大小写的问题
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError('图片验证码不一致')


        # 校验完成 需要把 attrs 返回
        return attrs


