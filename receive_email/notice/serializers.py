from rest_framework import serializers
from .models import Notice
import re


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = '__all__'

    def validate_email(self, value):
        pattern = r'^[a-zA-Z0-9._%+-]{4,}@cowave\.kr$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "이메일은 @cowave.kr로 끝나야 하며, 아이디는 최소 4글자 이상이어야 합니다.")
        return value
