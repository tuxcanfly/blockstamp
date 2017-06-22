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

from opentimestamps.core.timestamp import DetachedTimestampFile, make_merkle_tree
from opentimestamps.core.serialize import StreamSerializationContext
from opentimestamps.core.op import OpAppend, OpSHA256
from opentimestamps.cmds import create_timestamp
from opentimestamps.args import parse_ots_args

CALENDAR_URLS = [
        'https://a.pool.opentimestamps.org',
        'https://b.pool.opentimestamps.org',
        'https://a.pool.eternitywall.com',
]

logger = logging.getLogger(__name__)


def stamp_command(fd, args):
    # Create initial commitment ops for all files
    merkle_roots = []

    try:
        file_timestamp = DetachedTimestampFile.from_fd(OpSHA256(), fd)
    except OSError as exp:
        logging.error("Could not read %r: %s" % (fd.name, exp))
        return

    # Add nonce
    nonce_appended_stamp = file_timestamp.timestamp.ops.add(OpAppend(os.urandom(16)))
    merkle_root = nonce_appended_stamp.ops.add(OpSHA256())
    merkle_roots.append(merkle_root)
    merkle_tip = make_merkle_tree(merkle_roots)

    create_timestamp(merkle_tip, CALENDAR_URLS, parse_ots_args(args))

    try:
        with open("%s.ots" % fd.name, "wb") as timestamp_fd:
            ctx = StreamSerializationContext(timestamp_fd)
            file_timestamp.serialize(ctx)
    except IOError as exp:
        logger.error("Failed to create timestamp: %s" % exp)
        return


@receiver(post_save, sender=WebPage)
def page_save_handler(sender, instance, created, **kwargs):
    if created:
        response = requests.get(instance.url)
        body = fromstring(response.content)
        instance.title = body.findtext('.//title')

        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(instance.url))
        body.make_links_absolute(base_url)
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
