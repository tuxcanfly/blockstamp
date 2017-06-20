from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from stamper.models import WebPage
from stamper.serializers import WebPageSerializer


@api_view(['GET', 'POST'])
def page_list(request):
    if request.method == 'GET':
        pages = WebPage.objects.all()
        serializer = WebPageSerializer(pages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WebPageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def page_detail(request, pk):
    try:
        page = WebPage.objects.get(pk=pk)
    except WebPage.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WebPageSerializer(page)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WebPageSerializer(page, data=response.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        page.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
