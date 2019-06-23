# -*- coding: utf-8 -*-
'''
@Time    : 2019-06-20 16:41
@Author  : Leon
@Contact : wangdongjie1994@gmail.com
@File    : tasks.py
@Software: PyCharm
'''
from celery_tasks.main import celery_app
from celery_tasks.sms.utils.yuntongxun.sms import CCP
import logging

logger = logging.getLogger('django')

# 这里只是帮助咱们实现任务，具体的业务逻辑仍然放在Django视图函数里面,只管去帮助咱们处理任务，返回值仍然
# 视图函数执行
@celery_app.task(name= 'send_sms_code')   # 将任务加载到broker里面
def send_sms_code(mobile,sms_code,expires,temp_id):
    """发送短信验证码"""
    try:
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, expires], temp_id)

    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))

    else:
        if result == 0:
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)

        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)


