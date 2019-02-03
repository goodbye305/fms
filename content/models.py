#-*- coding: utf-8 -*-
'''
    Author: Geekwolf
    Blog: http://www.simlinux.com
'''
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.conf import settings
from accounts.models import User, Project
from content.storage import images_storage
import uuid


class Type(models.Model):
    id = models.UUIDField(blank=True, primary_key=True, auto_created=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, verbose_name=u"故障类型")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:

        permissions = (
            ("update_type", ("更新故障类型")),
            ("del_type", ("删除故障类型")),
        )
        default_permissions = ()


class Content(models.Model):
    fms_level = (
        (0, u"p0"),
        (1, u"p1"),
        (2, u"p2"),
        (3, u"p3"),
        (4, u"p4"),
    )
    fms_status = (
        (0, u"处理中"),
        (1, u"已恢复"),
        (2, u"改进中"),
        (3, u"已完结"),
    )
    fms_improve = (
        (0, u"开发"),
        (1, u"运维"),
        (2, u"机房"),
        (3, u"网络运营商"),
        (4, u"第三方"),

    )
    fms_type = Type.objects.all().values_list('id', 'name')
    fms_project = Project.objects.all().values_list('id', 'name')
    id = models.UUIDField(blank=True, primary_key=True, auto_created=True, default=uuid.uuid4)
    title = models.CharField(max_length=255, verbose_name=u'故障简述', unique=True)
    author = models.ForeignKey(to=User, verbose_name=u'创建者')
    level = models.IntegerField(choices=fms_level, verbose_name=u'故障级别')
    type = models.ForeignKey(
        Type, related_name='fms_type', verbose_name=u'故障类型', null=True)
    project = models.ForeignKey(Project, related_name='fms_project', verbose_name=u'影响项目', null=True, on_delete=models.PROTECT)
    effect = models.TextField(blank=True, verbose_name=u'故障影响')
    reasons = models.TextField(blank=True, verbose_name=u'故障原因', null=True)
    solution = models.TextField(blank=True, verbose_name=u'解决方案', null=True)
    status = models.IntegerField(choices=fms_status, verbose_name=u'故障状态')
    improve = models.IntegerField(choices=fms_improve, verbose_name=u'主导改进')
    content = models.TextField(blank=True, verbose_name=u'故障分析')
    start_time = models.DateTimeField(verbose_name=u'开始时间')
    end_time = models.DateTimeField(verbose_name=u'结束时间')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    deal_author = models.ForeignKey(to=User,related_name="deal_author",verbose_name=u'当前处理人')

    def __unicode__(self):
        return self.title

    class Meta:

        permissions = (
            ("get_content", ("查看故障列表")),
            ("detail_content", ("故障详情")),
            ("add_content", ("添加故障")),
            ("edit_content", ("编辑故障")),
            ("del_content", ("删除故障")),
        )
        default_permissions = ()


class ZbxContent(models.Model):

    fms_status = (
        (0, u"处理中"),
        (1, u"已恢复"),
        (2, u"改进中"),
        (3, u"已完结"),
    )

    id = models.UUIDField(blank=True, primary_key=True, auto_created=True, default=uuid.uuid4)
    eventid = models.IntegerField(unique=True, verbose_name=u'事件ID')
    title = models.CharField(max_length=255, verbose_name=u'故障简述')
    host = models.CharField(max_length=120, verbose_name='故障服务器Top10', null=True)
    author = models.CharField(max_length=10, default='ZABBIX', verbose_name=u'ZBX用户')
    level = models.CharField(max_length=60, verbose_name=u'故障级别')
    type = models.CharField(max_length=120, verbose_name=u'zbx应用集', blank=True, null=True)
    project = models.CharField(max_length=255, verbose_name=u'ZBX主机组')
    effect = models.TextField(blank=True, verbose_name=u'故障影响', null=True)
    reasons = models.TextField(blank=True, verbose_name=u'故障原因', null=True)
    solution = models.TextField(blank=True, verbose_name=u'解决方案', null=True)
    status = models.CharField(max_length=60, verbose_name=u'处理状态', default=u'未恢复')
    improve = models.CharField(max_length=10, default=u'运维', verbose_name=u'主导改进')
    content = models.TextField(blank=True, verbose_name=u'故障分析')
    start_time = models.DateTimeField(verbose_name=u'开始时间')
    end_time = models.DateTimeField(verbose_name=u'结束时间', null=True, blank=True)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')


class Images(models.Model):

    url = models.ImageField(upload_to='img/%Y/%m/%d', blank=True, null=True, storage=images_storage())
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
