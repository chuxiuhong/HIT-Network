#coding=utf8
import requests
from models import *

class Cache():
    def __init__(self, url):
        self.url = url

    def check_cache(self):
        '''
        检查是否有一致的缓存
        :return: Boolean型
        '''
        try:
            f = cache.objects.get(name=self.url)
            headers = {'If-Modified-Since': f.timestamp}
            if requests.get(self.url, headers=headers).status_code == 304:
                return True
            else:
                return False
        except:
            return False

    def update(self, content, content_type):
        '''
        更新缓存
        :param content: 内容
        :param content_type: 内容类型
        :return:
        '''
        try:
            f = cache.objects.get(name=self.url)
            f.content = content
            f.content_type = content_type
            f.name = self.url
            f.save()
        except:
            f = cache()
            f.content = content
            f.name = self.url
            f.content_type = content_type
            f.save()

    def get(self):
        #获取缓存
        f = cache.objects.get(name=self.url)
        return (f.content, f.content_type)
