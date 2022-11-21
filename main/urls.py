from os import name
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('getuserforms', views.APIGetUserForms)
router.register('getuserformsfilters', views.APIGetUserFormsDJFilters)
router.register('getuserformsparams', views.APIGetUserFormsParams)


urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('quiz/', views.QuizList.as_view(), name="quiz_list"),
    path('quiz/<pk>/<quest>', views.QuizPage.as_view(), name="quiz"),
    path('form/', views.FormPage.as_view(), name="form"),
    path('propose/', views.ProposePage.as_view(), name="propose"),
    path('api/', include(router.urls)),
    path('api/createform', views.APICreateUserForm, name="api_createform"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
