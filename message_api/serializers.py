from rest_framework import serializers

from message_api import models


class MessageSerializer(serializers.ModelSerializer):
	slug = serializers.SlugField(write_only=True)
	counter = serializers.IntegerField(read_only=True)

	class Meta:
		model = models.Message
		fields = (
			'slug',
			'text',
			'counter',
		)

	def update(self, instance, validated_data):
		validated_data['counter'] = 0
		return super(MessageSerializer, self).update(instance, validated_data)
