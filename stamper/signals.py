import io
import os
import sys

import logging

from urllib.parse import urlsplit

import bitcoin
import requests

from lxml.html import fromstring, tostring

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from stamper.models import WebPage
from stamper.utils import stamp_command

@receiver(post_save, sender=WebPage)
def page_save_handler(sender, instance, created, **kwargs):
    if created:
        response = requests.get(instance.url)
        body = fromstring(response.content)
        instance.title = body.findtext('.//title')

        body.make_links_absolute(instance.url)
        content = tostring(body)

        html_file_dir = "%s/%s/%s" % (settings.MEDIA_ROOT,
                settings.HTML_FILES, instance.id)
        os.mkdir(html_file_dir)
        html_file_name = "%s/%s.html" % (html_file_dir, instance.id)

        with open(html_file_name, "a+b") as html_file:
            html_file.write(content)
            html_file.seek(0)
            stamp_command(html_file, ['stamp', ])

        bitcoin.SelectParams(settings.BITCOIN_PARAMS)
        proxy = bitcoin.rpc.Proxy(settings.BITCOIN_NODE)
        instance.address = str(proxy.getnewaddress())

        instance.save()
