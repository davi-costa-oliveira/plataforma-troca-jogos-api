from django.contrib import admin
from .models import (
    Estado,
    Cidade,
    Categoria,
    User,
    Endereco,
    PreferenciaUsuario,
    SituacaoPost,
    Post,
    FotoPost,
    InteresseTrocaPost,
    SituacaoProposta,
    Proposta,
    FotoProposta
)

admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Categoria)
admin.site.register(User)
admin.site.register(Endereco)
admin.site.register(PreferenciaUsuario)
admin.site.register(SituacaoPost)
admin.site.register(Post)
admin.site.register(FotoPost)
admin.site.register(InteresseTrocaPost)
admin.site.register(SituacaoProposta)
admin.site.register(Proposta)
admin.site.register(FotoProposta)