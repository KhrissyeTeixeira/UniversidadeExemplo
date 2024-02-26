from django.urls import path
from .views import (Homepage, DetalhesTurmaView, DetalhesAlunoTurmaView, AbrirAulaView,
                    CustomPasswordChangeView, CustomLoginView, TurmasDeAlunoView, TurmasDeProfessorView,
                    CustomLogoutView)

urlpatterns = [
    # Página inicial
    path('', Homepage.as_view(), name='homepage'),

    # Rotas de autenticação
    path('login/', CustomLoginView.as_view(), name='login'),
    path('alterar-senha/', CustomPasswordChangeView.as_view(), name='alterar-senha'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    # Rotas para professores
    path('professor/<str:matricula>/', TurmasDeProfessorView.as_view(), name='lista_turmas_professor'),
    path('professor/<str:codigo_turma>/detalhes/', DetalhesTurmaView.as_view(), name='detalhes_turma'),
    path('professor/<str:codigo_turma>/abrir_aula/', AbrirAulaView.as_view(), name='abrir_aula'),

    # Rotas para alunos
    path('aluno/<str:matricula>/', TurmasDeAlunoView.as_view(), name='lista_turmas_aluno'),
    path('aluno/<str:codigo_turma>/<str:matricula_aluno>/detalhes/', DetalhesAlunoTurmaView.as_view(), name='detalhes_aluno_turma'),
]


