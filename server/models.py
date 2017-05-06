#coding=utf8
from django.db import models


class fish(models.Model):
    #钓鱼规则表
    user_ip = models.CharField(max_length=15) #客户ip
    forbidden_host = models.CharField(max_length=100)  #禁止的host
    fish_url = models.CharField(max_length=100)  #跳转的网站链接


class firewall(models.Model):
    #黑名单规则表
    user_ip = models.CharField(max_length=15)   #客户ip
    forbidden_host = models.CharField(max_length=100)  #禁止的host


class cache(models.Model):
    #缓存表
    timestamp = models.CharField(max_length=80) #时间戳
    name = models.CharField(max_length=150) #文件名对应的url
    content_type = models.CharField(max_length=50)  #内容类型
    content = models.TextField()  #内容


def check_if_replace(user_ip, host):
    user_list = firewall.objects.filter(user_ip=user_ip).all()  #先到黑名单中查找
    for user in user_list:
        if user.forbidden_host in host or host == '*':
            return (1, '<h1>You have been forbidden!</h1>') #返回禁止页
    general = firewall.objects.filter(user_ip='*').all()
    for i in general:
        if i.forbidden_host in host:
            return (1, '<h1>You have been forbidden!</h1>')
    fish_list = fish.objects.filter(user_ip=user_ip).all()  #然后到钓鱼规则中查找
    for fisher in fish_list:
        if fisher.forbidden_host in host:
            return (-1, fisher.fish_url)
    return (0, host)
