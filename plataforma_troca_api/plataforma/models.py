from django.db import models

class Categoria(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao


class Estado(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome



class Cidade(models.Model):
    nome = models.CharField(max_length=255)
    estado = models.ForeignKey(
        Estado,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    cidade = models.ForeignKey(
        Cidade,
        on_delete=models.CASCADE
    )
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.endereco

class User(models.Model):
    login = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255)
    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.nome
        

class PreferenciaUsuario(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

class SituacaoPost(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

class Post(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    descricaoProduto = models.CharField(max_length=255)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )
    situacaoPost = models.ForeignKey(
        SituacaoPost,
        on_delete=models.CASCADE,
        default=1
    )
    trocaTemporaria = models.BooleanField(default=False)
    tempo = models.BigIntegerField(blank=True, null=True)
 
    def __str__(self):
        return self.descricaoProduto

class FotoPost(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    foto = models.ImageField(upload_to='posts_images')

class InteresseTrocaPost(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )

class SituacaoProposta(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

class Proposta(models.Model):
    proponente = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    menssagem = models.CharField(max_length=255)
    descricaoProduto = models.CharField(max_length=255)
    situacaoProposta = models.ForeignKey(
        SituacaoProposta,
        on_delete=models.CASCADE
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE
    )
    trocaTemporaria = models.BooleanField(default=False)
    tempo = models.BigIntegerField(blank=True)

class FotoProposta(models.Model):
    proposta = models.ForeignKey(
        Proposta,
        on_delete=models.CASCADE
    )
    foto = models.ImageField(upload_to='propostas_images')




