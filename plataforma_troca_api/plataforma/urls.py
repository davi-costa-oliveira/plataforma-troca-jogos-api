from django.urls import (
    path,
    include,
)
from plataforma import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


router = DefaultRouter()
router.register('estado', views.EstadoViewSet),
router.register('cidade', views.CidadeViewSet),
router.register('categoria', views.CategoriaViewSet),
router.register('situacaoProposta', views.SituacaoProstaViewSet),
router.register('situacaoPost', views.SituacaoPostViewSet),
router.register('InteresseTrocaPost', views.InteresseTrocaPostViewSet),


urlpatterns = [
    path('user/', views.userView),
    path('', include(router.urls)),
    path('proposta/', views.PropostaView),
    path('post/', views.postView),
    path('feed/', views.getFeedUser),
    path('login/', views.login),
    path('post/foto/', views.FotoPostUploadView.as_view(), name='image-upload'),    
    path('proposta/foto/', views.FotoPropostaUploadView.as_view(), name='image-upload'),
]