from rest_framework import status
from rest_framework.renderers import JSONRenderer


# 导入控制返回的JSON格式的类
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:

            # print(renderer_context)
            # print(renderer_context["response"].status_code)

            # 响应的信息，成功和错误的都是这个
            # 成功和异常响应的信息，异常信息在前面自定义异常处理中已经处理为{'message': 'error'}这种格式
            # print(data)

            # 如果返回的data为字典
            if isinstance(data, dict):
                # 响应信息中有message和code这两个key，则获取响应信息中的message和code，并且将原本data中的这两个key删除，放在自定义响应信息里
                # 响应信息中没有则将msg内容改为请求成功 code改为请求的状态码
                msg = data.pop('message', '请求成功')
                code = data.pop('code', renderer_context["response"].status_code)
            # 如果不是字典则将msg内容改为请求成功 code改为请求的状态码
            else:
                msg = '请求成功'
                code = renderer_context["response"].status_code

            # 自定义返回的格式
            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)


def customExceptionHandler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)
    #print(exc)  #错误原因   还可以做更详细的原因，通过判断exc信息类型
    #print(context)  # 错误信息
    # print('1234 = %s - %s - %s' % (context['view'], context['request'].method, exc))
    #print(response)


    #如果response响应对象为空，则设置message这个key的值，并将状态码设为500
    #如果response响应对象不为空，则则设置message这个key的值，并将使用其本身的状态码
    if response is None:
        return Response({
            'message': '{exc}'.format(exc=exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        # print('123 = %s - %s - %s' % (context['view'], context['request'].method, exc))
        return Response({
            'message': '{exc}'.format(exc=exc),
        }, status=response.status_code, exception=True)
