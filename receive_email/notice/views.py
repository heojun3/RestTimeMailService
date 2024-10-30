# views.py
from rest_framework import viewsets
from .models import Notice
from .serializers import NoticeSerializer
from django.shortcuts import render


def index(request):
    return render(request, 'notice/notice_form.html')

###
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
