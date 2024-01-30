from django.db import models

# Create your models here.
class Member(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    passwd = models.CharField(max_length=50) 
    age = models.IntegerField()

    def __str__(self):
        return self.fname + ' ' + self.lname

# Tabela Escola
class Escola(models.Model):
    ID_Escola = models.BigAutoField(primary_key=True)
    Nome = models.CharField(max_length = 150)
    Agrupamento = models.CharField(max_length = 150)
    Localizacao = models.CharField(max_length = 100)

# Tabela Curso
class Curso(models.Model):
    ID_Curso = models.BigAutoField(primary_key=True)
    Nome = models.CharField(max_length=100)

# Tabela Turma
class Turma(models.Model):
    ID_Turma = models.BigAutoField(primary_key=True)
    ID_Escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    Nome = models.CharField(max_length=100)
    Numero_Alunos = models.IntegerField()
    ID_Curso = models.ForeignKey(Curso, models.CASCADE)

# Tabela Aluno
class Aluno(models.Model):
    ID_Aluno = models.BigAutoField(primary_key=True)
    ID_Turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    Nome = models.CharField(max_length=100)
    #Fotos = 

# Tabela Professor
class Professor(models.Model):
    ID_Professor = models.BigAutoField(primary_key=True)
    ID_Escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    Nome = models.CharField(max_length=100)

# Tabela Sala
class Sala(models.Model):
    ID_Sala = models.BigAutoField(primary_key=True)
    Nome_Sala = models.CharField(max_length=100)

# Tabela Horário
class Horario(models.Model):
    ID_Horario = models.BigAutoField(primary_key=True)
    ID_Sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    ID_Turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    ID_Professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    Hora_inicio = models.TimeField()
    Hora_fim = models.TimeField()
    Dia_semana = models.CharField(max_length=100)
    Disciplina = models.CharField(max_length=100)

# Tabela Falta
class Falta(models.Model):
    ID_Falta = models.BigAutoField(primary_key=True)
    ID_Aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    ID_Horario = models.ForeignKey(Horario, on_delete=models.CASCADE)


