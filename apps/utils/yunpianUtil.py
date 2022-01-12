import json
from utils.ypclient.yunpian import ClientV2

from django.conf import settings


class YunPian(object):
    def __init__(self):
        # api key
        self.client = ClientV2(settings.YUNPIAN_API_KEY)

    def send_register_sms(self, mobile, context):
        # 登录验证码短信
        tpl_id = settings.REGISTER_TPL_ID
        res = self.client.send_tpl_sms(
            mobile=mobile,
            tpl_id=tpl_id,
            tpl_context=context
        )
        print(json.dumps(res.json()))
        return res.json()
