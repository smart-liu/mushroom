import datetime
import random
import string

import oss2
from django.conf import settings


class RunOSS:
    def __init__(self, dirname=None):
        self.AccessKeyId = settings.OSS_AK
        self.AccessKeySecret = settings.OSS_SK
        self.Endpoint = settings.OSS_ENDPOINT
        self.BuckerName = settings.OSS_BUCKET_NAME
        self.dirname = dirname

    def getBucket(self):
        auth = oss2.Auth(self.AccessKeyId, self.AccessKeySecret)
        bucket = oss2.Bucket(auth, self.Endpoint, self.BuckerName)
        return bucket

    def uploadFIle(self, object_file, file_name):
        bucket = self.getBucket()
        now = datetime.datetime.now()
        random_name = now.strftime("%Y%m%d%H%M%S") + ''.join([random.choice(string.digits) for _ in range(4)])
        object_name = self.dirname + random_name + "." + file_name.split(".")[-1]
        f = object_file.read()
        try:
            ret = bucket.put_object(object_name, f)
            link = "https://{}.oss-cn-beijing.aliyuncs.com/".format(self.BuckerName) + object_name
            return {'status': ret.status, 'pay_certificate': link, 'objectname': object_name}
        except Exception as e:
            return e

    def deleteFIle(self, object_name):
        bucket = self.getBucket()
        try:
            ret = bucket.delete_object(object_name)
            return {'status': ret.status}
        except Exception as e:
            return e
