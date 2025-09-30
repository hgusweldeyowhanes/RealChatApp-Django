from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.utils import timezone
# Create your models here.


class LangLocale(models.Model):
    class ShortCode(models.TextChoices):
        AMHARIC = "am", _("Amharic")
        ENGLISH = "en", _("English")
        OROMIA = "orm", _("Afaan Oromia")
        FRENCH = "fr", _("French")

    name = models.CharField(max_length=150)
    shortcode = models.CharField(max_length=10, unique=True, choices=ShortCode.choices)
    logo = models.FileField(null=True)

    def __str__(self):
        return self.name.title()

class Configuration(models.Model):
    config_name = models.CharField(max_length=100, default="default")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Main Configuration"
        verbose_name_plural = "Main Confiugrations"

    def get(self, attribute, default=None):
        return self.__get(self, attribute, default)

    @classmethod
    def get_global(cls, attribute, default=None):
        configuration = cls.objects.first()

        return cls.__get(configuration, attribute, default), configuration

    @classmethod
    def get_attribute(cls, name, default=None):
        configuration = cls.objects.first()

        return cls.__get(configuration, name, default)

    @staticmethod
    def __get(configuration, attribute, default):
        if not configuration:
            return default

        if hasattr(configuration, attribute) and (
            getattr(configuration, attribute) is not None
        ):
            return getattr(configuration, attribute)

        return default
    @classmethod
    def start(cls):
        return cls.objects.first() or cls()

class FrontPageImageConfiguration(models.Model):
    class ImageLocation(models.IntegerChoices):
        MAIN_BANNER = 1, _("Main Banner")
        SIDE_BANNER = 2, _("Side Banner")
        CASINO_BANNER = 3, _("Casino Banner")
        POPUP_BANNER = 4, _("Popup Banner")
        LOGIN_BANNER = 5, _("Login Banner")
        SIGNUP_BANNER = 6, _("Sign-Up Banner")
        DEPOSIT_BANNER = 7, _("Deposit Banner")
        MOBILE_HEADER_BANNER = 8, _("Mobile Header Banner")

    class Channel(models.IntegerChoices):
        DESKTOP = 1, _("Desktop")
        MOBILE = 2, _("Mobile")
        BOTH = 3, _("Both")

    class Provider(models.IntegerChoices):
        CASINO = 1, _("Casino")
        SPORT = 2, _("Sport")
        BOTH = 3, _("Both")
    
    class Transition(models.TextChoices):
        NONE = "none", _("none")
        FADE = "fade", _("fade")
        SLIDE = "slide", _("slide")
        ZOOM = "zoom", _("zoom")
    

    photo = models.FileField(upload_to= "banners/original", validators= [FileExtensionValidator(['jpg', 'jpeg', 'png','webp'])])
    desktop_image = models.ImageField(upload_to = "banners/desktop", blank=True, null= True)
    tablet_image = models.ImageField(upload_to = "banners/tablet", blank = True, null = True)
    mobile_image = models.ImageField(upload_to = "banners/mobile", blank = True, null =True)
    cta_text = models.CharField(max_length=150,blank=True)
    cta_link = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    configuration = models.ForeignKey(
        "Configuration", related_name="front_page_images", on_delete=models.CASCADE
    )
    image_location = models.PositiveSmallIntegerField(
        choices=ImageLocation.choices, default=ImageLocation.MAIN_BANNER
    )
    image_channel = models.PositiveSmallIntegerField(
        choices=Channel.choices, default=Channel.BOTH
    )
    provider = models.PositiveSmallIntegerField(
        choices=Provider.choices, default=Provider.BOTH
    )

    image_link = models.CharField(max_length=150, blank=True)
    locale = models.ForeignKey(
        "LangLocale",
        null=True,
        blank=True,
        related_name="banner_images",
        on_delete=models.CASCADE,
    )
    transition_type = models.CharField(max_length=50,choices = Transition.choices ,default = Transition.NONE) 
    transition_duration = models.PositiveIntegerField(default=300)  

    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("order",)

    def optimize_image(self,image_field,width):
        if not image_field:
            return image_field
        img = Image.open(image_field)
        if img.mode in ("RGBA","LA","P"):
            img = img.convert("RGB")
        #resize image by maintaining aspect ratio
        w_percent = width/float(img.size[0])
        h_size = int(float(img.size[1])*w_percent)
        img = img.resize((width,h_size), Image.Resampling.LANCZOS)
        output = BytesIO()
        img.save(output, format='JPEG',quality=85,optimize = True)
        output.seek(0)
        return InMemoryUploadedFile(
            output, "image_field",
            f"{image_field.name.split('.')[0]}_{width}.jpg",
            "image/jpeg",
            output.getbuffer().nbytes ,None
        )
    def save(self, *args, **kwargs):
        old = None
        if self.pk:
            old = FrontPageImageConfiguration.objects.filter(pk = self.pk).first()
        if self.pk is None or (old and old.photo != self.photo.name):
            target_location = [
                self.ImageLocation.LOGIN_BANNER,
                self.ImageLocation.SIGNUP_BANNER,
                self.ImageLocation.DEPOSIT_BANNER,
                self.ImageLocation.MOBILE_HEADER_BANNER
            ]
            if self.photo and self.image_location in target_location:
                self.desktop_image= self.optimize_image(self.photo, width=1200)
                self.tablet_image = self.optimize_image(self.photo, width=900)
                self.mobile_image = self.optimize_image(self.photo, width=600)
        super().save(*args,  **kwargs)
         # Invalidate relevant cache banners
        for location in [self.image_location, None]:
            for channel in [self.image_channel, None]:
                for provider in [self.provider, None]:
                    key = f"banners_location_{location}_channel_{channel}_provider_{provider}"
                    cache.delete(key)
        
    def is_currently_active(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_time  and self.start_time > now:
            return False
        if self.end_time and self.end_time < now:
            return False
        return True
