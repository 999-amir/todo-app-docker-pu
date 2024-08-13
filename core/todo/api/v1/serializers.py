from rest_framework import serializers
from todo.models import TodoModel
from accounts.context_processors import profile_information


class TodoSerializer(serializers.ModelSerializer):
    # get model.job content with 20 first character
    snippet = serializers.ReadOnlyField(source='get_snippet')
    # get url of each object
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')

    class Meta:
        model = TodoModel
        fields = ['profile', 'level', 'snippet', 'job', 'is_done', 'absolute_url', 'dead_end', 'created', 'updated']
        read_only_fields = ['profile']

    # prevent to show snippet and absolute url in object (retrieve) and job in objects (list)
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet')
            rep.pop('absolute_url')
        else:
            rep.pop('job')
            # rep.pop('profile')
        return rep

    # function of get url of each object
    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    # make model.profile autofilled by logged in profile
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['profile'] = profile_information(request)['profile']
        return super().create(validated_data)
