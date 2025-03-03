from django.core.serializers import serialize
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic import (
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Post, Category
from .serializer import PostSerializer, CategorySerializer
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework import viewsets, filters
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from .pagination import Defaultpaginations


"""@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def api_post_list(request):
    if request.method=='GET':
        post = Post.objects.all()
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)
    elif request.method=='POST':
        seriallizer = PostSerializer(data=request.data)
        if seriallizer.is_valid():
            seriallizer.save()
            return Response(seriallizer.data)
        else:
            return Response(seriallizer.errors)
"""


#
# class PostList(APIView):
#     """change function base view to class base view"""
#     permission_classes=[IsAuthenticated]
#     serializer_class = PostSerializer
#
#     def get(self,request):
#         post = Post.objects.all()
#         serializer = self.serializer_class(post,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class PostList(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetail(GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request,*args,**kwargs)
#
#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)


# class PostDetail(RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
# def get(self,request,*args,**kwargs):
#     return self.retrieve(request,*args,**kwargs)
#
# def put(self, request, *args, **kwargs):
#     return self.update(request,*args,**kwargs)
#
# def delete(self,request,*args,**kwargs):
#     return self.destroy(request,*args,**kwargs)


# def list(self, request):
#     serializer = self.serializer_class(self.queryset, many=True)
#     return Response(serializer.data)
#
# def retrieve(self,request,pk=None):
#     post = Post.objects.get(pk=pk)
#     serializer = self.serializer_class(post)
#     return Response(serializer.data)
#
# def update(self, request,pk=None):
#     pass
#
# def destroy(self, request,pk=None):
#     pass
class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {"category": ["exact", "in"], "auther": ["exact"]}
    search_fields = ["title", "content"]
    ordering_fields = ["id"]
    pagination_class = Defaultpaginations


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
