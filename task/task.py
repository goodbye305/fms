from content import views as content_views
from content.models import Content, Type, User, Images, ZbxContent
import json
import time
import collections
from accounts.models import Contact
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from itertools import chain

def task():
    content = Content.objects.filter(status="0").select_related().all().order_by('-ctime')
    for i in list(content):
        print("content id is %d,mail is %s"%(i.id,i.deal_author.email))
        content_views.exec_send_waitdeal(i.id,i.deal_author.email.split(','))