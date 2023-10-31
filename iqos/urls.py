from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('order/', include('order.urls')),
]
#
# handler404 = 'main.views.not_found_page   '
# handler500 = 'main.views.server_error_page'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)