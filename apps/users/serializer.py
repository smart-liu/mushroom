import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ayc_mushroom.settings import REGEX_MOBILE
from users.models import User, VerifyCode, UserAddress, UserCompany


class AddressSerializer(serializers.ModelSerializer):
    """用户地址"""

    class Meta:
        model = UserAddress
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    """用户公司"""

    class Meta:
        model = UserCompany
        fields = ("name", "duties", "expertise", "qualifications", "create_time")


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    address = AddressSerializer(many=True)
    company = CompanySerializer()

    class Meta:
        model = User
        fields = ("id", "username", "nick_name", "gender", "email", "mobile", "is_active", "is_superuser",
                  "avatar", "address", "company")


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 },
                                 help_text="验证码")
    mobile = serializers.CharField(label="手机号", help_text="手机号", required=True, allow_blank=False,
                                   validators=[UniqueValidator(queryset=User.objects.all(), message="手机号已经存在")])
    nick_name = serializers.CharField(label="昵称", help_text="昵称", required=True, allow_blank=False)
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    # 字段级验证
    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]

            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    # 对象级验证
    def validate(self, attrs):
        attrs["username"] = attrs["mobile"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("nick_name", "code", "mobile", "password")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nick_name", "avatar", "email", "birthday")


class SmsCodeSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')

    class Meta:
        model = UserAddress
        exclude = ("update_time", )
