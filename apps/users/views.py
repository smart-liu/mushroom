import os
from random import choice

from django.db.models import Q
from rest_framework import status as drf_status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.conf import settings

from utils import serviceLogger
from utils.ossUtil import RunOSS
from utils.permissions import IsOwnerOrReadOnly
from utils.yunpianUtil import YunPian
from users.models import User, VerifyCode, UserAddress
from users.serializer import UserRegSerializer, UserDetailSerializer, SmsCodeSerializer, UserUpdateSerializer, \
    UserAddressSerializer


def jwtResponsePayloadHandler(token, user=None, request=None):
    """
    自定义返回字段
    """
    serviceLogger.info("获取用户信息")
    return {
        'user_id': user.id,
        'username': user.username,
        'nick_name': user.nick_name,
        'is_superuser': user.is_superuser,
        'allow_post': user.allow_post,
        'last_login': user.last_login,
        'token': token
    }


class UserViewset(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    create:
        创建用户
    update:
        更新用户信息
    read:
        获取用户详情
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # 设置认证方式
    authentication_classes = (JSONWebTokenAuthentication, )
    # 设置必须登录才能访问的权限类
    permission_classes = [IsAuthenticated, ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserUpdateSerializer

    def get_permissions(self):
        if self.action == "create":
            return []
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # 密码加密
        request.data["password"] = make_password(request.data["password"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["username"] = user.username
        re_dict["user_id"] = user.id

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=drf_status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class SmsCodeViewset(CreateModelMixin, GenericViewSet):
    """获取验证码"""
    serializer_class = SmsCodeSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian()

        code = self.generate_code()

        sms_status = yun_pian.send_register_sms(mobile=mobile, context={"code": code})

        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=drf_status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=drf_status.HTTP_201_CREATED)


class UploadApiView(APIView):
    """
    create:
        文件上传
    delete：
        删除文件
    """
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES['file']
        file_name = file.name
        oss = RunOSS(dirname=settings.OSS_UPLOAD_IMG_DIR)
        ret = oss.uploadFIle(object_file=file, file_name=file_name)
        status = ret.get("status")
        if status == 200:
            file_url = ret['pay_certificate']
            result_dict = {
                "file_url": file_url,
                "filename": file_name
            }
            return Response(result_dict, status=drf_status.HTTP_201_CREATED)
        else:
            return Response(data="文件上传失败", status=drf_status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        file_url = request.data["file_url"]
        url_split = file_url.split("/")
        object_name = url_split[-2] + "/" + url_split[-1]
        oss = RunOSS(dirname=settings.OSS_UPLOAD_IMG_DIR)
        ret = oss.deleteFIle(object_name=object_name)
        status = ret.get("status")
        if status == 204:
            return Response(status=drf_status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=drf_status.HTTP_400_BAD_REQUEST)


class UserAddressViewSet(ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, )
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
