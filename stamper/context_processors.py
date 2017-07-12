from django.conf import settings


def conf(request):
    return {"bitcoin_params": settings.BITCOIN_PARAMS}
