from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from youTube_app.models import DownloadUser, VidData, TemporaryUrl

# Register your models here.
UserAdmin.fieldsets += (
    'File_Location', {
        'fields': (
            'download_path',
            'downloads',
            'user_pic',
        )
    },
),

admin.site.register(DownloadUser, UserAdmin)
admin.site.register(VidData)
admin.site.register(TemporaryUrl)
