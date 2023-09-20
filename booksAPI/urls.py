from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from store.views import BookViewSet, auth, UserBooksRelationView
# from django.conf.urls import url


router = SimpleRouter()

# router.register(r'book', BookViewSet)
# router.register(r'book_relation', UserBooksRelationView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += router.urls
