import io
import os
import sys

import logging

from lxml.html import fromstring

from django.db.models.signals import post_save
from django.dispatch import receiver
from stamper.models import WebPage

from opentimestamps.core.timestamp import DetachedTimestampFile, make_merkle_tree
from opentimestamps.core.serialize import StreamSerializationContext
from opentimestamps.core.op import OpAppend, OpSHA256
from opentimestamps.cmds import create_timestamp
from opentimestamps.args import parse_ots_args

from archiveis import archiveis

ots_args = ['stamp', ]

calendar_urls = [
        'https://a.pool.opentimestamps.org',
        'https://b.pool.opentimestamps.org',
        'https://a.pool.eternitywall.com',
]

logger = logging.getLogger(__name__)


def stamp_command(fd):
    # Create initial commitment ops for all files
    merkle_roots = []

    try:
        file_timestamp = DetachedTimestampFile.from_fd(OpSHA256(), fd)
    except OSError as exp:
        logger.error("Could not read :%s" % exp)
        return

    # Add nonce
    nonce_appended_stamp = file_timestamp.timestamp.ops.add(OpAppend(os.urandom(16)))
    merkle_root = nonce_appended_stamp.ops.add(OpSHA256())
    merkle_roots.append(merkle_root)
    merkle_tip = make_merkle_tree(merkle_roots)

    create_timestamp(merkle_tip, calendar_urls, parse_ots_args(ots_args))

    try:
        with io.BytesIO() as timestamp_fd:
            ctx = StreamSerializationContext(timestamp_fd)
            file_timestamp.serialize(ctx)
            timestamp_fd.seek(0)
            return timestamp_fd.read()
    except IOError as exp:
        logger.error("Failed to create timestamp: %s" % exp)
        return


@receiver(post_save, sender=WebPage)
def page_save_handler(sender, instance, created, **kwargs):
    if created:
        try:
            url, body = archiveis.capture(instance.url)
            instance.title = fromstring(body.content).findtext('.//title')
            instance.body = body.content

            with io.BytesIO() as fd:
                fd.write(body.content)
                fd.seek(0)
                ts = stamp_command(fd)

            if ts != None:
                instance.signature = ts

        except Exception as e:
            logger.error("Failed to stamp url %s: %s" % (instance.url, e))
        instance.save()
