from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path("api/academics/", include("academics.urls")),
    path("api/", include("questions.urls")),
    path("api/", include("quizzes.urls")),
    path("api/", include("progress.urls")),
]
