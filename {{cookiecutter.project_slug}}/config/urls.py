from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views import defaults as default_views
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
admin.site.site_header = _('{{ cookiecutter.project_name }} Admin')
urlpatterns += [
    path(settings.ADMIN_URL, admin.site.urls),
]

# API URLs
# Create a router and register our resources with it.
urlpatterns += [
    # V1
    # JWT Token
    path('api/v1/auth/jwt/token/', obtain_jwt_token),
    path('api/v1/auth/jwt/refresh/', refresh_jwt_token),
    path('api/v1/auth/jwt/verify/', verify_jwt_token),
    {% if cookiecutter.use_oauth == 'y' -%}
    # OAuth
    path('api/v1/auth/oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    {%- endif %}
    # Docs
    path('api/v1/docs/', include_docs_urls(title='{{ cookiecutter.project_name }} API', public=False)),
    # Endpoints
    path('api/v1/', include('config.router', namespace="api_v1")),

]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
