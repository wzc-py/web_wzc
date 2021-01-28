from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from courseapp.models import Course
from web_wzch.settings.constants import IMG_SRC


class CartViewSet(ViewSet):
    """购物车"""

    # 只有登录且认证成功的用户才能访问
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def add_cart(self, request):
        course_id = request.data.get('course_id')
        # 认证成功的用户信息会被保存在request模块的user中
        user_id = request.user.id
        # 是否勾选
        select = True
        # 有效期 0为永久
        expire = 0
        # 校验前端传递的参数
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': "参数有误，课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            redis_connection = get_redis_connection('cart')
            # 多次操作redis 建议使用管道
            pipeline = redis_connection.pipeline()
            # 开启管道
            pipeline.multi()
            # 保存商品信息已经对应的有效期
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 保存商品的勾选状态
            pipeline.sadd('select_%s' % user_id, course_id)
            # 执行
            pipeline.execute()

            # 获取购物车商品数量
            cart_len = redis_connection.hlen('cart_%s' % user_id)
        except:
            return Response({"message": "购物车添加失败"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "购物车添加成功", "cart_length": cart_len})

    def list_cart(self, request):
        """展示购物车"""
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        cart_list_byte = redis_connection.hgetall('cart_%s' % user_id)
        select_list_byte = redis_connection.smembers('selected_%s' % user_id)

        # 循环从mysql获取课程信息
        data = []
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            try:
                course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)
            except Course.DoesNotExist:
                continue

            data.append({
                "selected": True if course_id_byte in select_list_byte else False,
                "course_img": IMG_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_id": expire_id,
                "price": course.price
            })

        return Response(data)

    def put(self, request):
        """切换购物车商品勾选状态"""
        user_id = request.user.id
        course_id = request.data.get("course_id")
        is_selected = request.data.get("is_selected")

        try:
            redis = get_redis_connection("cart")
            if is_selected:
                redis.sadd("selected_%s" % user_id, course_id)
            else:
                redis.srem("selected_%s" % user_id, course_id)
        except:
            return Response({"message": "购物车数据操作有误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "切换勾选状态成功！"})

    def delete(self, request):
        """删除商品"""
        user_id = request.user.id
        course_id = request.query_params.get("course_id")

        redis = get_redis_connection("cart")
        redis.hdel("cart_%s" % user_id, course_id)
        redis.srem("selected_%s" % user_id, course_id)

        return Response({"message": "删除商品成功!"}, status=status.HTTP_204_NO_CONTENT)
