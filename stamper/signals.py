import io
import os
import sys

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


def stamp_command(fd):
    # Create initial commitment ops for all files
    merkle_roots = []

    try:
        file_timestamp = DetachedTimestampFile.from_fd(OpSHA256(), fd)
    except OSError as exp:
        logging.error("Could not read :%s" % exp)
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
            return timestamp_fd
    except IOError as exp:
        logging.error("Failed to create timestamp: %s" % exp)
        return


@receiver(post_save, sender=WebPage)
def page_save_handler(sender, instance, created, **kwargs):
    if created:
        url, body = archiveis.capture(instance.url)
        with io.BytesIO() as fd:
            fd.write(body.content)
            ts = stamp_command(fd)

        instance.body = body.content
        if ts != None:
            instance.signature = ts

        instance.save()
