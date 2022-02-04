from django.contrib import admin
from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView



urlpatterns = [
    path('', include("shop.urls")),
    path('user/', include("user.urls")),
    path('admin/' , admin.site.urls),
    path('accounts/', include('user.urls')),
    path('payments/', include('payments.urls')),
    path('blog/', include('blog.urls')),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "rendOlives.views.page_not_found_view"
hnadler500 = "rendOlives.views.server_error"