#coding=utf8
import re
from contextlib import closing
from django.http import HttpResponse,HttpResponseRedirect
from Cache import *
def home(request):
    url = request.path[1:].split('/')
    url = url[0] + '//' + url[1] + '/'
    url = request.path[1:].replace(':/', '://')  #获得目标url
    host = request.get_host()
    method = request.method
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']  #获取客户端ip
    else:
        ip = request.META['REMOTE_ADDR']
    regex = re.compile('^HTTP_')
    headers = dict((regex.sub('', header), value) for (header, value)
                   in request.META.items() if header.startswith('HTTP_'))
    if len(request.REQUEST.items()) > 0:
        url += '?'
        for (i, j) in request.REQUEST.items():
            url += str(i) + '=' + str(j) + '&'
        url = url[:-1]  #将带参数的get请求恢复成原始链接状态
    check_tuple = check_if_replace(ip, host)
    if check_tuple[0] == 1:
        return HttpResponse(check_tuple[1])  #如果符合黑名单规则，返回禁止页
    elif check_tuple[0] == -1:
        url = check_tuple[1]
        return HttpResponseRedirect(url)   #如果符合钓鱼规则，那么重定向到指定的网站
    cacher = Cache(url)
    if cacher.check_cache():      #检查是否有与目标网站一致的资源
        res = cacher.get()
        return HttpResponse(res[0], content_type=res[1])  #将缓存的内容返回
    else:
        with closing(requests.request(method, url, headers=headers, data=request.POST, stream=True)) as r:
            cacher.update(bytes(r.content), content_type=r.headers['content-type'])  #更新缓存
            return HttpResponse(bytes(r.content), status=r.status_code, content_type=r.headers['content-type'])  #返回资源
