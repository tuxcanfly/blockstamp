from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from stamper.models import WebPage
from stamper.serializers import WebPageSerializer


@csrf_exempt
def page_list(request):
    if request.method == 'GET':
        pages = WebPage.objects.all()
        serializer = WebPageSerializer(pages, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = WebPageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def page_detail(request, pk):
    try:
        page = WebPage.objects.get(pk=pk)
    except WebPage.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = WebPageSerializer(page)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = WebPageSerializer(page, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        page.delete()
        return HttpResponse(status=204)
