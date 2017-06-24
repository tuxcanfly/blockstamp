from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

import bitcoin

from stamper.models import WebPage
from stamper.utils import stamp_command


class Command(BaseCommand):
    help = 'Handles payments'

    def handle(self, *args, **options):
        bitcoin.SelectParams(settings.BITCOIN_PARAMS)
        proxy = bitcoin.rpc.Proxy(settings.BITCOIN_NODE)

        for page in WebPage.objects.filter(status=0):
            if proxy.getreceivedbyaddress(page.address) >= settings.BITCOIN_FEE:
                page.status = 1
                page.save()
                html_file_dir = "%s/%s/%s" % (settings.MEDIA_ROOT,
                        settings.HTML_FILES, page.id)
                html_file_name = "%s/%s.html" % (html_file_dir, page.id)
                with open(html_file_name, "rb") as html_file:
                    args = ['--bitcoin-node=%s' % settings.BITCOIN_NODE, 'stamp', '--btc-wallet']
                    if settings.BITCOIN_PARAMS == "testnet":
                        args.insert(1, '--btc-testnet')
                    stamp_command(html_file, args)
                    page.status = 2
                    page.save()
