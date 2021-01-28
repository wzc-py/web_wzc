import random


def get_random_code():
    """生成随机验证啊"""
    code = ''
    for i in range(6):
        one_number = str(random.randint(0, 9))
        code += one_number
    return code
