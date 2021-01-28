import random

from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status

from userapp.models import UserInfo
from userapp.serializers import UserModelSerializer
from web_wzch.libs.geetest import GeetestLib
from userapp.utils import get_user_by_account
from web_wzch.settings import constants
from web_wzch.utils.random_code import get_random_code
from web_wzch.utils.send_message import Message

pc_geetest_id = "45dbe199c830b4b9cb1bebd76fbbfdb7"
pc_geetest_key = "cbdff4cfb81c08cb1312f36b963fec22"


class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        """获取验证码"""

        # 根据用户名验证当前用户是否存在
        account = request.query_params.get("username")
        user = get_user_by_account(account)

        if user is None:
            return Response({"message": "用户不存在"}, status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        print(self.status)
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        """校验验证码"""

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge", '')
        validate = request.data.get("geetest_validate", '')
        seccode = request.data.get("geetest_seccode", '')
        account = request.data.get('username')
        user = get_user_by_account(account)

        if user:
            # 验证结果是否正确
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)

# 用户注册
class UserAPIView(CreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class MessageAPIView(APIView):
    def get(self, request, *args, **kwargs):
        """
        获取验证码  为手机号生成验证码并发送
        """
        phone = request.query_params.get("phone")

        # TODO 1. 判断手机号是否在60s内发送过短信
        redis_connection = get_redis_connection("sms_code")
        mobile = redis_connection.get("sms_%s" % phone)

        if mobile is not None:
            return Response({"message": "您已经在60s内发送过短信了"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        # TODO 2. 为当前手机号生成随机验证码
        code = get_random_code()

        # TODO 3. 将验证码保存到redis中
        # 验证码发送的间隔时间
        redis_connection.setex("sms_%s" % phone, constants.SMS_EXPIRE_TIME, code)
        # 保存验证的有效时间
        redis_connection.setex("exp_%s" % phone, constants.MOBILE_EXPIRE_TIME, code)

        # TODO 4. 调用方法  完成短信发送
        try:
            message = Message(constants.API_KEY)
            message.send_message(phone, code)
        except:
            return Response({"message": "短信发送失败，请稍后再试"},
                            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # TODO 5. 将发送结果响应到前端
        return Response({"message": "发送短信成功"}, status=http_status.HTTP_200_OK)
