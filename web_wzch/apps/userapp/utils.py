from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from userapp.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        'user_id': user.id
    }


def get_user_by_account(account):
    try:
        # 三者只要满足其中一个条件 则返回查询到用户
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account) | Q(email=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user


class UserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据条件查询用户
        user = get_user_by_account(username)

        if user and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None
