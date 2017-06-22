import os
import logging

from opentimestamps.core.timestamp import DetachedTimestampFile, make_merkle_tree
from opentimestamps.core.serialize import StreamSerializationContext, StreamDeserializationContext, BadMagicError, DeserializationError
from opentimestamps.core.op import OpAppend, OpSHA256
from opentimestamps.cmds import create_timestamp, verify_timestamp
from opentimestamps.args import parse_ots_args

from bitcoin.core import b2x

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

def verify_command(fd, target_fd, args):
    ctx = StreamDeserializationContext(fd)
    try:
        detached_timestamp = DetachedTimestampFile.deserialize(ctx)
    except BadMagicError:
        logging.error("Error! %r is not a timestamp file." % fd.name)
        return False
    except DeserializationError as exp:
        logging.error("Invalid timestamp file %r: %s" % (fd.name, exp))
        return False

    if target_fd is None:
        # Target not specified, so assume it's the same name as the
        # timestamp file minus the .ots extension.
        if not fd.name.endswith('.ots'):
            logging.error('Timestamp filename does not end in .ots')
            return False

        target_filename = fd.name[:-4]
        logging.info("Assuming target filename is %r" % target_filename)

        try:
            target_fd = open(target_filename, 'rb')
        except IOError as exp:
            logging.error('Could not open target: %s' % exp)
            return False

    logging.debug("Hashing file, algorithm %s" % detached_timestamp.file_hash_op.TAG_NAME)
    actual_file_digest = detached_timestamp.file_hash_op.hash_fd(target_fd)
    logging.debug("Got digest %s" % b2x(actual_file_digest))

    if actual_file_digest != detached_timestamp.file_digest:
        logging.debug("Expected digest %s" % b2x(detached_timestamp.file_digest))
        logging.error("File does not match original!")
        return False

    return verify_timestamp(detached_timestamp.timestamp, parse_ots_args(args))
