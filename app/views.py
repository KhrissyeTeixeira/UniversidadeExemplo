from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.checks import messages

from .models import Usuario
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render, redirect

from .forms import EmailLoginForm
from .models import Aluno, Professor, Turma, Aula, Presenca, Matricula
from django.utils import timezone


class ProfessorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'professor')

    def handle_no_permission(self):
        # Redireciona para a homepage se o usuário não for um professor
        return redirect('homepage')


# TurmasDeAlunoView
class TurmasDeAlunoView(LoginRequiredMixin, TemplateView):
    template_name = 'app/turma/lista_turmas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matricula_aluno = self.kwargs.get('matricula')
        aluno = get_object_or_404(Aluno, matricula=matricula_aluno)
        context['turmas'] = Turma.objects.filter(matriculados__aluno=aluno)
        context['pessoa'] = aluno
        return context


# TurmasDeProfessorView
class TurmasDeProfessorView(LoginRequiredMixin, TemplateView):
    template_name = 'app/turma/lista_turmas_professor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matricula_professor = self.kwargs.get('matricula')
        professor = get_object_or_404(Professor, matricula=matricula_professor)
        context['turmas'] = professor.turmas.all()
        context['pessoa'] = professor
        return context


class DetalhesTurmaView(LoginRequiredMixin, ProfessorRequiredMixin, TemplateView):
    template_name = 'app/turma/detalhes_turma.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        codigo_turma = self.kwargs.get('codigo_turma')
        turma = get_object_or_404(Turma, codigo=codigo_turma)
        aulas = Aula.objects.filter(turma=turma).order_by('data').prefetch_related('presencas')
        matriculas = Matricula.objects.filter(turma=turma).order_by('aluno__nome')
        alunos = [matricula.aluno for matricula in matriculas]

        total_aulas = aulas.count()

        # Adicionando informações de presença para cada aluno em cada aula
        for aluno in alunos:
            aluno.presencas_count = 0  # Inicializa o contador de presenças para cada aluno

        for aula in aulas:
            aula.presencas_list = []
            for aluno in alunos:
                presenca = aula.presencas.filter(aluno=aluno).first()
                is_presente = presenca.presente if presenca else False
                aula.presencas_list.append({
                    'aluno': aluno,
                    'presente': is_presente
                })
                if is_presente:
                    aluno.presencas_count += 1  # Incrementa o contador se o aluno estava presente

        # Calcula a porcentagem de presença para cada aluno
        for aluno in alunos:
            aluno.presenca_percentual = (aluno.presencas_count / total_aulas) * 100 if total_aulas > 0 else 0

        context['turma'] = turma
        context['aulas'] = aulas
        context['alunos'] = alunos
        context['total_aulas'] = total_aulas
        return context


class DetalhesAlunoTurmaView(LoginRequiredMixin, TemplateView):
    template_name = 'app/turma/detalhes_aluno_turma.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        codigo_turma = self.kwargs.get('codigo_turma')
        matricula_aluno = self.kwargs.get('matricula_aluno')

        turma = get_object_or_404(Turma, codigo=codigo_turma)
        aluno = get_object_or_404(Aluno, matricula=matricula_aluno)
        aulas = Aula.objects.filter(turma=turma).order_by('data').prefetch_related('presencas')
        total_aulas = aulas.count()

        aluno.presencas_count = 0
        aluno.presencas_list = []

        for aula in aulas:
            presenca = aula.presencas.filter(aluno=aluno).first()
            is_presente = presenca.presente if presenca else False
            aluno.presencas_list.append({
                'aula': aula,
                'presente': is_presente
            })
            if is_presente:
                aluno.presencas_count += 1

        aluno.presenca_percentual = (aluno.presencas_count / total_aulas) * 100 if total_aulas > 0 else 0

        context['turma'] = turma
        context['aluno'] = aluno
        context['aulas'] = aulas
        context['total_aulas'] = total_aulas
        return context


class Homepage(TemplateView):
    template_name = 'homepage.html'


#class TurmasMatriculaView(LoginRequiredMixin, TemplateView):
 #   template_name = 'app/turma/lista_turmas.html'

  #  def get_context_data(self, **kwargs):
   #     context = super().get_context_data(**kwargs)
    #    matricula = self.kwargs.get('matricula')

     #   aluno = Aluno.objects.filter(matricula=matricula).first()
      #  professor = Professor.objects.filter(matricula=matricula).first()

       # if aluno:
        #    context['turmas'] = Turma.objects.filter(matriculados__aluno=aluno)
         #   context['pessoa'] = aluno
        #elif professor:
         #   context['turmas'] = professor.turmas.all()
          #  context['pessoa'] = professor
       # else:
        #    context['erro'] = 'Matrícula não encontrada.'

       # return context


class AbrirAulaView(LoginRequiredMixin, ProfessorRequiredMixin, TemplateView):
    template_name = 'app/turma/abrir_aula.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        codigo_turma = self.kwargs.get('codigo_turma')
        turma = get_object_or_404(Turma, codigo=codigo_turma)
        context['turma'] = turma

        # Aqui, você precisa de uma maneira de obter a matrícula do professor logado
        # Exemplo: supondo que o professor logado está disponível como 'request.user.professor'
        # e que o professor tem um atributo 'matricula'
        matricula_professor = self.request.user.professor.matricula
        context['pessoa'] = self.request.user.professor  # ou somente matricula_professor

        return context

    def post(self, request, *args, **kwargs):
        codigo_turma = self.kwargs.get('codigo_turma')
        turma = get_object_or_404(Turma, codigo=codigo_turma)

        # Criar nova aula
        nova_aula = Aula.objects.create(turma=turma, data=timezone.now())

        # Registrar presenças
        codigos_rfid = request.POST.get('codigos_rfid', '').split('\n')
        for codigo in codigos_rfid:
            codigo_limpo = codigo.strip()
            if codigo_limpo:
                aluno = Aluno.objects.filter(ip=codigo_limpo).first()
                if aluno:
                    Presenca.objects.create(aula=nova_aula, aluno=aluno, presente=True)

        # Redirecionar para a página de detalhes da turma
        return redirect('detalhes_turma', codigo_turma=codigo_turma)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        # Loga o usuário
        super().form_valid(form)
        user = form.get_user()

        # Verifica se o email do usuário corresponde a um Aluno ou Professor
        aluno = Aluno.objects.filter(email=user.email).first()
        if aluno:
            return redirect('lista_turmas_aluno', matricula=aluno.matricula)

        professor = Professor.objects.filter(email=user.email).first()
        if professor:
            return redirect('lista_turmas_professor', matricula=professor.matricula)

        # Redireciona para a página inicial para outros tipos de usuários
        return redirect('homepage')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')  # Redirecione para a página de login após a alteração da senha
    template_name = 'alterar_senha.html'  # Especifique o template para a página de alteração de senha

    def form_valid(self, form):
        form.save()  # Salva a nova senha
        messages.success(self.request, 'Sua senha foi alterada com sucesso!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')  # Redireciona para página de login após o logout