from banners import  models
from rest_framework import serializers


class LanguageLocaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LangLocale
        fields = "__all__"

class FrontPageImageConfigurationSerializer(serializers.ModelSerializer):
    locale = LanguageLocaleSerializer()
    image_location_display = serializers.CharField(source='get_image_location_display', read_only=True)
    image_channel_display = serializers.CharField(source='get_image_channel_display', read_only=True)
    provider_display = serializers.CharField(source='get_provider_display', read_only=True)

    class Meta:
        model = models.FrontPageImageConfiguration
        fields = [
            "id",
            "photo",
            "desktop_image",
            "tablet_image",
            "mobile_image",
            "cta_text",
            "cta_link",
            "image_location_display",
            "image_channel_display",
            "provider_display",
            "transition_type",
            "transition_duration",
            "locale"
        ]
        read_only_fields = ['desktop_image', 'tablet_image', 'mobile_image']
