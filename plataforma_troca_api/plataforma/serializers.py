from rest_framework import serializers
from plataforma.models import (
    User,
    Estado,
    Post,
    FotoPost,
    InteresseTrocaPost,
    Cidade,
    Categoria,
    Proposta,
    FotoProposta,
    SituacaoPost,
    SituacaoProposta
)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for Parametros."""

    class Meta:
        model = User
        fields = ['id', 'login', 'senha', 'nome', 'email', 'telefone', 'endereco']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create(
            **validated_data
        )
        return user

class PostSerializer(serializers.ModelSerializer):
    """Serializer for Parametros."""

    class Meta:
        model = Post
        fields = ['id', 'usuario', 'descricaoProduto', 'categoria','situacaoPost', 'trocaTemporaria', 'tempo']
        read_only_fields = ['id']

        def create(self, validated_data):
            print(validated_data)
            post = Post.objects.create(
                **validated_data
            )
            return post


class PropostaSerializer(serializers.ModelSerializer):
    """Serializer for Parametros."""

    class Meta:
        model = Proposta
        fields = ['id', 'proponente', 'post', 'menssagem', 'descricaoProduto', 'situacaoProposta', 'categoria', 'trocaTemporaria', 'tempo']
        read_only_fields = ['id']

        def create(self, validated_data):
            print(validated_data)
            proposta = Proposta.objects.create(
                **validated_data
            )
            return proposta


class EstadoSerializer(serializers.ModelSerializer):
    """Serializer for Parametros."""

    class Meta:
        model = Estado
        fields = ['id', 'nome']
        read_only_fields = ['id']

class CidadeSerializer(serializers.ModelSerializer):
    """Serializer for Cidade."""

    class Meta:
        model = Cidade
        fields = ['id', 'nome', 'estado']
        read_only_fields = ['id']

class CategoriaSerializer(serializers.ModelSerializer):
    """Serializer for Categoria."""

    class Meta:
        model = Categoria
        fields = ['id', 'descricao']
        read_only_fields = ['id']

class InteresseTrocaPostSerializer(serializers.ModelSerializer):
    """Serializer for InteresseTrocaPost."""

    class Meta:
        model = InteresseTrocaPost
        fields = ['post', 'categoria']

class SituacaoPostSerializer(serializers.ModelSerializer):
    """Serializer for SituacaoPost."""

    class Meta:
        model = SituacaoPost
        fields = ['id', 'descricao']

class SituacaoPropostaSerializer(serializers.ModelSerializer):
    """Serializer for SituacaoProposta."""

    class Meta:
        model = SituacaoProposta
        fields = ['id', 'descricao']

class FotoPostSerializer(serializers.ModelSerializer):
    """Serializer for FotoPost."""

    class Meta:
        model = FotoPost
        fields = ['post', 'foto']

class FotoPropostaSerializer(serializers.ModelSerializer):
    """Serializer for FotoProposta."""

    class Meta:
        model = FotoProposta
        fields = ['proposta', 'foto']
        


