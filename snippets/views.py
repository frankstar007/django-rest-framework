#coding:utf-8
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# Create your views here.

# class JSONResponse(HttpResponse):
#     """docstring for JSONRenderer"""
#     '''
#     将HttpResponse对象相应的内容转化为json
#     '''
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    '''
    显示所有的snippets的对象,或者创建一个新的对象
    '''
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)

        return Response(serializers.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializers = SnippetSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def snippet_detail(request, pk, format=None):
    '''
    查找、更新或者删除一个snippet
    '''
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
