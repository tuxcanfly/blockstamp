from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from stamper.models import WebPage
from stamper.utils import verify_command


class Command(BaseCommand):
    help = 'Updates stamps'

    def handle(self, *args, **options):
        for page in WebPage.objects.filter(status=0):
            ots_filename = "%s/%s/%s/%s.html.ots" % (settings.MEDIA_ROOT,
                settings.HTML_FILES, page.id, page.id)
            with open(ots_filename, "rb") as fd:
                if verify_command(fd, None, ["verify", ots_filename]):
                    page.status = 1
                    page.save()
