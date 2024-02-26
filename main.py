import os
import django

# Defina a variável de ambiente DJANGO_SETTINGS_MODULE para apontar para o módulo de configurações do seu projeto.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AccessCTRL")

# Configure o Django.
django.setup()

import datetime
from app.models import Aluno, Professor, Turma, Presenca


def cadastrar_aluno():
    print("Cadastro de Aluno")
    matricula = int(input("Matrícula: "))
    nome = input("Nome: ")
    email = input("Email: ")
    foto = input("Caminho da foto: ")
    ip = input("IP: ")

    aluno = Aluno(matricula=matricula, nome=nome, email=email, foto=foto, ip=ip)
    aluno.save()
    print(f"Aluno {nome} cadastrado com sucesso!")


def cadastrar_professor():
    print("Cadastro de Professor")
    matricula = int(input("Matrícula: "))
    nome = input("Nome: ")
    email = input("Email: ")
    foto = input("Caminho da foto: ")
    ip = input("IP: ")

    professor = Professor(matricula=matricula, nome=nome, email=email, foto=foto, ip=ip)
    professor.save()
    print(f"Professor {nome} cadastrado com sucesso!")


def controle_presenca():
    ip = input("Digite o IP do professor para abrir a aula: ")

    try:
        professor = Professor.objects.get(ip=ip)
    except Professor.DoesNotExist:
        professor = None

    if professor:
        # Abra a aula e permita o controle de presença
        turma_aberta = Turma.objects.filter(professor=professor).first()

        if not turma_aberta:
            print("Não há nenhuma aula aberta para esse professor.")
        else:
            print(f"Aula aberta: {turma_aberta.nome}")
            while True:
                ip_aluno = input("Digite o IP do aluno (ou IP do professor para encerrar a aula): ")
                if ip_aluno == ip:
                    # Professor digitou seu próprio IP para encerrar a aula
                    break

                try:
                    aluno = Aluno.objects.get(ip=ip_aluno)
                    presenca, created = Presenca.objects.get_or_create(aluno=aluno, turma=turma_aberta,
                                                                       data=datetime.date.today())
                    if created:
                        print(f"Presença registrada para {aluno.nome}.")
                    else:
                        print(f"Presença já registrada para {aluno.nome}.")
                except Aluno.DoesNotExist:
                    print("Aluno não encontrado ou aula não está aberta.")

    else:
        print("IP não pertence a um professor.")


if __name__ == "__main__":
    while True:
        opcao = input("Escolha uma opção (cadastro / controle de presença / sair): ")
        if opcao == "cadastro":
            tipo_usuario = input("Digite 'aluno' ou 'professor': ")
            if tipo_usuario == "aluno":
                cadastrar_aluno()
            elif tipo_usuario == "professor":
                cadastrar_professor()
            else:
                print("Opção inválida.")
        elif opcao == "controle de presença":
            controle_presenca()
        elif opcao == "sair":
            break
        else:
            print("Opção inválida. Escolha 'cadastro', 'controle de presença' ou 'sair'.")
