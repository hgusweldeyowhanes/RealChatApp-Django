from django.shortcuts import render
from rest_framework import serializers,generics,permissions
from rest_framework.response import Response
from banners import models
from django.core.cache import cache
from django.db.models import Q
from banners import serializers
from django.utils import timezone
from rest_framework.exceptions import ValidationError
# Create your views here.

class BannerListView(generics.ListAPIView):
    serializer_class = serializers.FrontPageImageConfigurationSerializer

    def get_permissions(self):
        location = self.request.GET.get("location")
        
        if location and int(location) == models.FrontPageImageConfiguration.ImageLocation.DEPOSIT_BANNER:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()] 
    
    # def get_queryset(self):
    #     """get filtered and cached queryset of banners
    #     """
    #     cache_key = self._generate_cache_key()
    #     cached_queryset = cache.get(cache_key)
    #     if cached_queryset is not None:
    #         return cached_queryset
        
    #     queryset = models.FrontPageImageConfiguration.objects.filter(is_active = True)
    #     queryset = self._apply_filters(queryset)
    #     queryset = self._apply_time_filters(queryset)
    #     queryset = queryset.order_by('order')
    #     cache.set(cache_key,queryset,300)
    #     return queryset
    
    # def _generate_cache_key(self):

    #     location = self.request.GET.get("location")
    #     channel = self.request.GET.get("channel")
    #     provider = self.request.GET.get("provider")

    #     return f"banners_location_{location}_channel_{channel}_provider_{provider}"
    
    # def _apply_filters(self,queryset):

    #     location = self.request.GET.get("location")
    #     channel = self.request.GET.get("channel")
    #     provider = self.request.GET.get("provider")

    #     if location:
    #         try:
    #             location_int = int(location)
    #             valid_locations = [choice[0] for choice in models.FrontPageImageConfiguration.ImageLocation.choices]
    #             if location_int not in valid_locations:
    #                 raise ValidationError({"location": "Invalid location value"})
    #             queryset = queryset.filter(image_location=location_int)
    #         except (ValueError, TypeError):
    #             raise ValidationError({"location": "Location must be a valid integer"})
    
    #     if channel:
    #         try:
    #             channel_int = int(channel)
    #             valid_channels = [choice[0] for choice in models.FrontPageImageConfiguration.Channel.choices]
    #             if channel_int not in valid_channels:
    #                 raise ValidationError({"channel": "Invalid channel value"})
    #             # Include BOTH option in addition to the specific channel
    #             queryset = queryset.filter(
    #                 Q(image_channel=channel_int) | 
    #                 Q(image_channel=models.FrontPageImageConfiguration.Channel.BOTH)
    #             )
    #         except (ValueError, TypeError):
    #             raise ValidationError({"channel": "Channel must be a valid integer"})
        
    #     # Filter by provider
    #     if provider:
    #         try:
    #             provider_int = int(provider)
    #             valid_providers = [choice[0] for choice in models.FrontPageImageConfiguration.Provider.choices]
    #             if provider_int not in valid_providers:
    #                 raise ValidationError({"provider": "Invalid provider value"})
    #             # Include BOTH option in addition to the specific provider
    #             queryset = queryset.filter(
    #                 Q(provider=provider_int) | 
    #                 Q(provider=models.FrontPageImageConfiguration.Provider.BOTH)
    #             )
    #         except (ValueError, TypeError):
    #             raise ValidationError({"provider": "Provider must be a valid integer"})
        
    #     return queryset

    # def _apply_time_filters(self, queryset):
    #     """
    #     Apply time-based filters to show only currently active banners
    #     """
    #     now = timezone.now()
        
    #     return queryset.filter(
    #         Q(start_time__lte=now) | Q(start_time__isnull=True),
    #         Q(end_time__gte=now) | Q(end_time__isnull=True)
    #     )

    # def list(self, request, *args, **kwargs):
    #     """
    #     Override list method to handle empty responses gracefully
    #     """
    #     try:
    #         queryset = self.get_queryset()
            
    #         # Return empty array if no banners found (fallback handling)
    #         if not queryset.exists():
    #             return Response([])
            
    #         # Serialize the data
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data)
            
    #     except ValidationError as e:
    #         # Return validation errors
    #         return Response(e.detail, status=400)
    #     except Exception as e:
    #         # Log the error and return a generic error message
    #         # In production, you'd want to use proper logging
    #         print(f"Error retrieving banners: {e}")
    #         return Response(
    #             {"error": "An unexpected error occurred while retrieving banners"}, 
    #             status=500
    #         )
    def get_queryset(self):
        """Return filtered and cached banners"""
        cache_key = self._cache_key()
        if (cached := cache.get(cache_key)) is not None:
            return cached

        queryset = (
            models.FrontPageImageConfiguration.objects.filter(is_active=True)
            .order_by("order")
        )
        queryset = self._apply_filters(queryset)
        queryset = self._apply_time_filters(queryset)

        cache.set(cache_key, queryset, timeout=300)
        return queryset

    def _cache_key(self):
        """Generate unique cache key based on filters"""
        params = {k: self.request.GET.get(k) for k in ["location", "channel", "provider"]}
        return "banners_" + "_".join(f"{k}_{v}" for k, v in params.items())

    def _apply_filters(self, queryset):
        """Validate and apply location, channel, and provider filters"""
        filters = {
            "location": (models.FrontPageImageConfiguration.ImageLocation.choices, "image_location"),
            "channel": (models.FrontPageImageConfiguration.Channel.choices, "image_channel"),
            "provider": (models.FrontPageImageConfiguration.Provider.choices, "provider"),
        }

        for param, (choices, field) in filters.items():
            value = self.request.GET.get(param)
            if not value:
                continue

            try:
                value_int = int(value)
            except (ValueError, TypeError):
                raise ValidationError({param: f"{param.capitalize()} must be an integer"})

            valid_values = [choice[0] for choice in choices]
            if value_int not in valid_values:
                raise ValidationError({param: f"Invalid {param} value"})

            # Include BOTH option if available
            if hasattr(models.FrontPageImageConfiguration, param.capitalize()):
                both = getattr(models.FrontPageImageConfiguration, param.capitalize()).BOTH
                queryset = queryset.filter(Q(**{field: value_int}) | Q(**{field: both}))
            else:
                queryset = queryset.filter(**{field: value_int})

        return queryset

    def _apply_time_filters(self, queryset):
        """Show only currently active banners"""
        now = timezone.now()
        return queryset.filter(
            Q(start_time__lte=now) | Q(start_time__isnull=True),
            Q(end_time__gte=now) | Q(end_time__isnull=True),
        )

    def list(self, request, *args, **kwargs):
        """Graceful response if no banners or validation errors"""
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                return Response([])
            return Response(self.get_serializer(queryset, many=True).data)
        except ValidationError as e:
            return Response(e.detail, status=400)
        except Exception as e:
            # Proper logging should replace print in real production
            print(f"Error retrieving banners: {e}")
            return Response(
                {"error": "Unexpected error occurred while retrieving banners"},
                status=500,
            )
