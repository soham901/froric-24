from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('apps.core.urls')),
    path('demo/', include('apps.demo.urls')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
)
