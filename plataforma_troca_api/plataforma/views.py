from django.shortcuts import render, get_object_or_404
from plataforma import serializers
from rest_framework.parsers import JSONParser
from rest_framework import (
    viewsets,
    mixins,
)
from plataforma.models import (
    User,
    Estado,
    Cidade,
    PreferenciaUsuario,
    Categoria,
    Endereco,
    Post,
    FotoPost,
    SituacaoPost,
    InteresseTrocaPost,
    FotoPost,
    Proposta,
    FotoProposta,
    SituacaoProposta
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.core import serializers as serializejson
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
import os 

def createOrUpDateUser(request):
    if request.method=='PUT':
        #deleta o endereço e preferencias do banco para recriar
        endereco = Endereco.objects.filter(user = request.data['id'])
        endereco.delete()

        preferenciasUsuario = PreferenciaUsuario.objects.filter(usuario_id = request.data['id'])
        for pu in preferenciasUsuario:
            pu.delete()

    cid = Cidade.objects.filter(id = request.data['endereco']['cidade'])

    endereco = Endereco.objects.create(
        cidade = cid[0],
        endereco = request.data['endereco']['endereco'],
        numero = request.data['endereco']['numero'],
        complemento = request.data['endereco']['complemento']
    )

    if request.method=='PUT':
        user, created = User.objects.update_or_create(
            id = request.data['id'],
            login = request.data['login'],
            senha = request.data['senha'],
            nome = request.data['nome'],
            email = request.data['email'],
            telefone = request.data['telefone'],
            endereco = endereco,
        )

    if request.method=='POST':
        user = User.objects.create(
            login = request.data['login'],
            senha = request.data['senha'],
            nome = request.data['nome'],
            email = request.data['email'],
            telefone = request.data['telefone'],
            endereco = endereco,
        )
    print(user)

    for pref in request.data['preferencias']:
        categoria = Categoria.objects.filter(id = pref)
        PreferenciaUsuario.objects.create(
            usuario = user,
            categoria = categoria[0]
        )

    return user

@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def postView(request):
    if request.method=='GET' and 'user_id' in request.GET:
        posts = Post.objects.filter(usuario_id = request.query_params['user_id'])
        return JsonResponse(loadListPostsInformationJSON(posts), safe=False)

    if request.method=='GET' and 'post_id' in request.GET:
        posts = get_object_or_404(Post.objects.all(), pk=request.query_params['post_id'])
        return JsonResponse(loadPostsInformationJSON(posts), safe=False)

    if request.method=='POST':
        post_serializer = serializers.PostSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='PUT':
        post = get_object_or_404(Post.objects.all(), pk=request.data['id'])
        post_serializer = serializers.PostSerializer(post,data=request.data, partial=True)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE' and 'post_id' in request.GET:
        posts = get_object_or_404(Post.objects.all(), pk=request.query_params['post_id'])
        posts.delete()
        return JsonResponse("Deleted Successfully", status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def PropostaView(request):
    if request.method=='GET' and 'user_id' in request.GET:
        proposta = Proposta.objects.filter(proponente_id = request.query_params['user_id'])
        return JsonResponse(loadListPropostaInformationJSON(proposta), safe=False)

    if request.method=='GET' and 'proposta_id' in request.GET:
        proposta = get_object_or_404(Proposta.objects.all(), pk=request.query_params['proposta_id'])
        return JsonResponse(loadPropostaInformationJSON(proposta), safe=False)

    if request.method=='POST':
        proposta_serializer = serializers.PropostaSerializer(data=request.data)
        if proposta_serializer.is_valid():
            proposta_serializer.save()
            return Response(proposta_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(proposta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='PUT':
        proposta = get_object_or_404(Proposta.objects.all(), pk=request.data['id'])
        proposta_serializer = serializers.PropostaSerializer(proposta,data=request.data, partial=True)
        if proposta_serializer.is_valid():
            proposta_serializer.save()
            return Response(proposta_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(proposta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='DELETE' and 'proposta_id' in request.GET:
        proposta = get_object_or_404(Proposta.objects.all(), pk=request.query_params['proposta_id'])
        proposta.delete()
        return JsonResponse("Deleted Successfully", status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def userView(request):
    if request.method=='GET' and 'user_id' in request.GET:
        user = User.objects.filter(id = request.query_params['user_id'])
        print(userToJSON(user[0]))
        return JsonResponse(userToJSON(user[0]), safe=False)

    if request.method=='POST':
        if(User.objects.filter(login = request.data['login'])):
            return Response({"msg": "login em uso"})
        return Response(userToJSON(createOrUpDateUser(request)), status=status.HTTP_201_CREATED)
        

    if request.method=='PUT':
        user = get_object_or_404(User.objects.all(), pk=request.data['id'])
        if(User.objects.filter(Q(login = request.data['login']), ~Q(id = request.data['id']))):
            return Response({"msg": "login em uso"})
        return Response(userToJSON(createOrUpDateUser(request)), status=status.HTTP_201_CREATED)

    if request.method=='DELETE' and 'user_id' in request.GET:
        user = get_object_or_404(User.objects.all(), pk=request.query_params['user_id'])
        endereco = Endereco.objects.filter(user = request.query_params['user_id'])
        endereco.delete()
        user.delete()        
        
        return JsonResponse("Deleted Successfully", status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['GET'])
def getFeedUser(request):
    
    if 'user_id' in request.GET:
        #Pega os posts que dão macth com o perfil do usuario passado como parametro
        userID = request.query_params['user_id']
        posts = Post.objects.raw(f"""
        select *  from plataforma_post 
        where 
        usuario_id != {userID} AND
        situacaoPost_id = 1 AND
        categoria_id in (
            select categoria_id from plataforma_preferenciaUsuario WHERE usuario_id = {userID}
        )
        """)
        userMacthes = loadListPostsInformationJSON(posts)

        #Pega os posts que dão macth com os posts do usuario passado como parametro
        postsFromUser = Post.objects.filter(usuario_id = userID, situacaoPost_id=1)
        postMatches = []
        if(postsFromUser):
            for p in postsFromUser:
                result = Post.objects.raw(f"""
                select *  from plataforma_post p
                join plataforma_InteresseTrocaPost itp on p.id = itp.post_id
                where 
                p.usuario_id != {userID} AND
                p.situacaoPost_id = 1 AND
                p.categoria_id in (select categoria_id from plataforma_InteresseTrocaPost WHERE post_id = {p.id}) AND
                itp.categoria_id in (select categoria_id from plataforma_post WHERE id = {p.id})
                """)
                if(result):
                    postMatches = merge_json_lists(loadListPostsInformationJSON(result),postMatches)

        #Pega 30 posts aleatorios para completar o feed
        randomPosts = Post.objects.filter(situacaoPost=1).order_by('?')[:30]

        result = merge_json_lists(userMacthes, postMatches)
        result =  merge_json_lists(result, loadListPostsInformationJSON(randomPosts))

        return JsonResponse(result, safe=False)
    else:
        #Retorna 30 posts aleatorios
        randomPosts = Post.objects.filter(situacaoPost=1).order_by('?')[:30]
        return JsonResponse(loadListPostsInformationJSON(randomPosts), safe=False)
    


@api_view(['POST'])
def login(request):
    loginUsuario = request.data['login']
    senhaUsuario = request.data['senha']

    for u in User.objects.raw(f"select * from plataforma_user where login = '{loginUsuario}' and senha = '{senhaUsuario}'"):
        return Response({
            "id": u.id,
            "nome": u.nome
            }) 
        
    return Response({"message": "Usuario não encontrado"}, status=status.HTTP_400_BAD_REQUEST) 

class FotoPostUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = serializers.FotoPostSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            fotoPost = FotoPost.objects.get(id= request.query_params['id'])
            image_file = fotoPost.foto.path
            fotoPost.delete()
            print(image_file)
            if os.path.exists(image_file):
                os.remove(image_file)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FotoPost.DoesNotExist:
            return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

class FotoPropostaUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = serializers.FotoPropostaSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            fotoProposta = FotoProposta.objects.get(id= request.query_params['id'])
            image_file = fotoProposta.foto.path
            fotoProposta.delete()
            print(image_file)
            if os.path.exists(image_file):
                os.remove(image_file)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FotoProposta.DoesNotExist:
            return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)



class InteresseTrocaPostViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    """Manage InteresseTrocaPost in the database."""
    serializer_class = serializers.InteresseTrocaPostSerializer
    queryset = InteresseTrocaPost.objects.all()

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset

class EstadoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    """Manage Estado in the database."""
    serializer_class = serializers.EstadoSerializer
    queryset = Estado.objects.all()

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset

class CidadeViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    """Manage Estado in the database."""
    serializer_class = serializers.CidadeSerializer
    queryset = Cidade.objects.all()

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset

class SituacaoProstaViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    """Manage SituacaoProposta in the database."""
    serializer_class = serializers.SituacaoPropostaSerializer
    queryset = SituacaoProposta.objects.all()

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset

class SituacaoPostViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    """Manage SituacaoPost in the database."""
    serializer_class = serializers.SituacaoPostSerializer
    queryset = SituacaoPost.objects.all()

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset

class CategoriaViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    """Manage Estado in the database."""
    serializer_class = serializers.CategoriaSerializer
    queryset = Categoria.objects.all()

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset

def userToJSON(user):
    print(user)
    return {
        "id": user.id,
        "login": user.login,
        "senha": user.senha,
        "nome": user.nome,
        "email": user.email,
        "telefone": user.telefone,
        "endereco":{
            "cidade":  user.endereco.cidade.nome,
            "endereco": user.endereco.endereco,
            "numero": user.endereco.numero,
            "complemento": user.endereco.complemento
        }
    }

def merge_json_lists(list1, list2):
    merged_list = list1 + list2
    unique_objects = {}
    result_list = []
    for json_obj in merged_list:
        object_id = json_obj['post']['id']
        if object_id not in unique_objects:
            unique_objects[object_id] = object_id
            result_list.append(json_obj)
    return result_list

def loadPostsInformationJSON(post):
    postJson = {}
    postJson['post'] =  {
        "id": post.id,
        "usuario": post.usuario.id,
        "descricaoProduto": post.descricaoProduto,
        "categoria": post.categoria.descricao,
        "situacaoPost": post.situacaoPost.descricao,
        "trocaTemporaria": post.trocaTemporaria,
        "tempo": post.tempo
    }

    fotos = FotoPost.objects.filter(post = post)
    fotosURLs = []
    if(fotos):
        for foto in fotos:
            fotosURLs.append({
                "id": foto.id,
                "url": foto.foto.path
            })
        postJson['fotos'] = fotosURLs

    interesseTrocaPosts = InteresseTrocaPost.objects.filter(post = post)
    if(interesseTrocaPosts):
        categorias = []
        for interesseTrocaPost  in interesseTrocaPosts:
            categorias.append({
                "idInteresseTrocaPosts": interesseTrocaPost.id,
                "url": interesseTrocaPost.categoria.id
            })

        postJson['interesseTrocaPost'] = categorias

    return postJson

def loadListPostsInformationJSON(posts):
    result = []
    if (posts):
        for post in posts:
            result.append(loadPostsInformationJSON(post))
    return result

def loadPropostaInformationJSON(proposta):

    propostaJson = {}
    propostaJson['proposta'] =  {
        "id": proposta.id,
        "proponente": proposta.proponente.id,
        "post": proposta.post.id,
        "menssagem": proposta.menssagem,
        "descricaoProduto": proposta.descricaoProduto,
        "categoria": proposta.categoria.descricao,
        "situacaoProposta": proposta.situacaoProposta.descricao,
        "trocaTemporaria": proposta.trocaTemporaria,
        "tempo": proposta.tempo
    }

    fotos = FotoProposta.objects.filter(proposta = proposta)
    fotosURLs = []
    if(fotos):
        for foto in fotos:
            fotosURLs.append({
                "id": foto.id,
                "url": foto.foto.path
            })
        propostaJson['fotos'] = fotosURLs

    return propostaJson

def loadListPropostaInformationJSON(propostas):
    result = []
    if (propostas):
        for proposta in propostas:
            result.append(loadPropostaInformationJSON(proposta))
    return result