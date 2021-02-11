from django.db.models import fields
from rest_framework import serializers

from .models import UserScript
from .processing import db


class ScriptListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Сериализатор для списка скриптов.
    """
    author = serializers.StringRelatedField(many=False)
    url = serializers.HyperlinkedIdentityField(view_name='api-script-detail', read_only=True)
    
    class Meta:
        model = UserScript
        fields = ['author', 'name', 'description', 'url']


class ScriptDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной информации и результатов скрипта.
    """
    results = serializers.SerializerMethodField()

    class Meta:
        model = UserScript
        fields = ['name', 'script', 'results']

    def get_results(self, obj):
        headers, results, error = db.get_info(obj.script)
        if not error:
            return headers, results
        else:
            return error


class ScriptAddSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления новых скриптов.
    """
    class Meta:
        model = UserScript
        fields = ['name', 'description', 'script']
