from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser, User


class Usuario(AbstractUser):
    matricula = models.CharField(max_length=20, blank=True, null=True)


class Professor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='professor', null=True, blank=True)
    matricula = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ip = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        if not self.usuario:
            # Cria um usuário com o e-mail como username e senha
            try:
                self.usuario = Usuario.objects.create_user(username=self.email, email=self.email, password=self.email)
            except IntegrityError:
                # Lidar com o caso de e-mail duplicado ou nome de usuário
                pass
        super(Professor, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='aluno', null=True, blank=True)
    matricula = models.CharField(max_length=20)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ip = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.usuario:
            # Cria um usuário com o e-mail como username e senha
            try:
                self.usuario = Usuario.objects.create_user(username=self.email, email=self.email, password=self.email)
            except IntegrityError:
                # Lidar com o caso de e-mail duplicado ou nome de usuário
                pass
        super(Aluno, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.matricula} - {self.nome}"


class Turma(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, related_name='turmas', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='matriculas')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='matriculados')

    def __str__(self):
        return f"{self.aluno.nome} - {self.turma.nome}"


class Aula(models.Model):
    turma = models.ForeignKey(Turma, related_name='aulas', on_delete=models.CASCADE)
    data = models.DateField()

    def __str__(self):
        return f"Aula de {self.turma.nome} em {self.data}"


class Presenca(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='presencas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='presencas')
    presente = models.BooleanField(default=False)

    class Meta:
        unique_together = ('aula', 'aluno')

    def __str__(self):
        return f"{self.aula.turma.nome} - {self.aluno.nome} - {'Presente' if self.presente else 'Ausente'}"
