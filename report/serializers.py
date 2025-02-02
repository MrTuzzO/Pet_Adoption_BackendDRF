from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(source='reporter.username', read_only=True)
    post_title = serializers.CharField(source='post.name', read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'reporter', 'reporter_username', 'post', 'post_title', 'reason', 'description', 'created_at',
                  'status', 'admin_feedback']
        read_only_fields = ['status', 'admin_feedback']