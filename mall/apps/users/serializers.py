import re
from rest_framework import serializers
from users.models import User,Address
from django_redis import get_redis_connection
# serializers.ModelSerializer
# serializers.Serializer

# 数据入库  选择 ModelSerializer 肯定有 模型
class RegisterCreateUserSeaializer(serializers.ModelSerializer):

    """
    6个参数(username,password,password2,mobile,sms_code,allow)

    ModelSerializer   在自动生成字段的时候 是根据fields生成的我们自动写的字段
    也要添加到 fields列表里

    """

    # read_only 只去读取,不写入
    # User 模型中没有这个 属性,也就是 说 这个字段 我们只要 传入,不能 读取
    # r  w

    sms_code = serializers.CharField(label='短信验证码',min_length=6,max_length=6,write_only=True)
    password2 = serializers.CharField(label='确认密码',write_only=True)
    allow = serializers.CharField(label='确认密码',write_only=True)
    # ModelSerializer 自动生成字段的时候 是根据 fields 列表生成的

    # token = serializers.CharField(label='token',required=False)
    token = serializers.CharField(label='token',read_only=True)

    class Meta:
        model = User
        fields = ['username','password','mobile', 'sms_code', 'password2', 'allow','token']

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }


    """
    1.字段类型
    2.字段选项
    3.单个字段
    4.多个字段




    1.手机号校验,密码一致,短信校验,是否同意

    手机号就是规则 单个字段
    是否同意  单个字段

    密码一致,短信校验       多个字段
    """

    def validate_mobile(self,value):

        if not re.match('1[3-9]\d{9}',value):
            raise serializers.ValidationError('手机号不满足规则')
        # 校验之后最终要返回回去
        return value

    def validate_allow(self,value):

        if value == 'false':
            raise serializers.ValidationError('您未同意协议')

        return value

    def validate(self, attrs):

        # 1.密码一致
        password = attrs.get('password')
        password2 = attrs.get('password2')
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms_code')

        if password  != password2:
            raise serializers.ValidationError('密码不一致')

        # 2. 短信

        redis_conn = get_redis_connection('code')

        sms_code_redis = redis_conn.get('sms_%s'%mobile)
        if sms_code_redis is None:
            raise serializers.ValidationError('验证码已过期')

        if sms_code_redis.decode()  != sms_code:
            raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validated_data):

        # 的时候 {'password2': '1234567890', 'mobile': '18310820688', 'username': 'itcast', 'password': '1234567890', 'sms_code': '081702', 'allow': 'true'}
         # 多了字段
        #  User.objects.create(**validated_data)
        # 删除多余字段
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # user = User.objects.create(**validated_data)
        user = super().create(validated_data)

        # 修改密码
        user.set_password(validated_data['password'])
        user.save()

        # 生成token
        from rest_framework_jwt.settings import api_settings

        # 获取jwt的2个方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # payload 可以装载数据(用户数据)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)


        user.token = token


        return user

# class Person(object):
# name = 'abc'
#
# p = Person()
# p.name = 'itcast'
# # 给对象动态添加属性
#  p.age = 10
# p2 = Person()
# print(p2.age)




# serializers.ModelSerializer
# serializers.Serializer
class UserCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email','email_active')


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


    # def update(self, instance, validated_data):


class AddressSerializer(serializers.ModelSerializer):

    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')


    def create(self, validated_data):

        # 我们并没有让前端传递用户的的 user_id 因为 我们是采用的jwt认证方式
        # 我们可以获取user_id 所以 validated_data 没有user_id
        # 但是我们在调用 系统的 crate方法的时候  Address.objects.create(**validated_data)
        # Address必须要 user_id 这个外键,所以就报错了
        # user = request.user

        validated_data['user'] = self.context['request'].user

        # return Address.objects.create(**validated_data)

        # super() 指向 单继承的 ModelSerializer

        return super().create(validated_data)


