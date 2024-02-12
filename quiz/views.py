import json
import uuid

import pytz
import redis, json
import vaex
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q, Count, Avg, Subquery, OuterRef, Sum
from braces.views import JsonRequestResponseMixin, CsrfExemptMixin
from django.db.models.functions import ExtractDay, ExtractYear

from django.contrib.auth.decorators import permission_required
from account.models import Organizations, CustomUser
from account.utils.recent_activity import RecentActivity
# models
from .models import Quiz, Question, Answer, Result, Category, ExcelFileUploaded
from .forms import QuestionForm, QuizForm, answer_formset, ExportExcelQuestion

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, date, timedelta, timezone
import requests
import pandas as pd
from uuid import uuid4

from django.views.decorators.cache import cache_page

r = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT
)


# Create your views here.

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/dashboard.html'

    # @cache_page(60 * 15)
    def get(self, request):
        print('hello')
        if request.user.is_superuser or request.user.is_staff:
            return redirect('quiz:manage_dashboard')
        categories = Category.objects.filter(parent__isnull=True)[:7]
        end_date = datetime.today()
        st_date = end_date - timedelta(days=7)
        results = Result.objects.filter(user=request.user, quiz__module__isnull=True).select_related(
            'quiz__category__parent')

        return self.render_to_response({
            'object_list': categories,
            'results': results
        })


dashboard = Dashboard.as_view()


class QuizHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/quiz_home.html'

    # @cache_page(60 * 15)
    def get(self, request, slug=None, *args, **kwargs):

        if slug is not None:
            today = datetime.now(pytz.timezone('Asia/Tashkent'))
            quiz = Quiz.objects.filter(category_id=OuterRef('pk'), period_date__isnull=False, period_date__gte=today,
                                       module__isnull=True)

            categories = Category.objects.filter(parent__slug=slug).annotate(quiz=Subquery(quiz.values('id')[:1]), )


        else:
            categories = Category.objects.filter(level=0).order_by('name').distinct('name').values('name',
                                                                                                   'level',
                                                                                                   'icon',
                                                                                                   'quizs',
                                                                                                   'slug',
                                                                                                   'children')

        return self.render_to_response({
            'object_list': categories,
        })

        # if slug is not None:
        #     categories = Category.objects.prefetch_related('quizs').filter(parent__slug=slug)
        # else:
        #     categories = Category.objects.all()
        #
        # return self.render_to_response({
        #     'object_list': categories,
        #     # 'cat': cat
        # })


quiz_home = QuizHomeView.as_view()


class UserQuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quiz/user_quiz_list.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(active=True, period_date__gte=datetime.now(tz=pytz.timezone('Asia/Tashkent')),
                                   category__slug=self.kwargs['quiz_slug'])
        return queryset


user_quiz_list_view = UserQuizListView.as_view()


class UserQuizDetail(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'quiz/detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        try:
            result = get_object_or_404(Result, user=self.request.user, quiz=self.object)
        except:
            result = None
        resent = RecentActivity(self.request.user)
        if self.object.course:
            title = f"{self.object.category}-{self.object.course}"
        else:
            title = f"{self.object.category}"
        data = {
            'date': datetime.now().timestamp(),
            'category': 'test',
            'title': title,
            'url': self.request.path
        }
        resent.add_resent_activity(data)

        context['result'] = result
        return context


user_quiz_detail = UserQuizDetail.as_view()


class QuizStart(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/quiz_start.html'

    def get(self, request, pk):
        request.session['user'] = f"{datetime.now()}"
        quiz = get_object_or_404(Quiz, pk=pk)
        result = Result.objects.filter(quiz=quiz)
        # if result[0].attempts > 3:
        #     return redirect('/')
        return self.render_to_response({
            'quiz': quiz
        })

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = None
        return HttpResponse(request.POST)
        # return self.render_to_response({
        #     'data': questions,
        #     'time': 10,
        # })


quiz_start = QuizStart.as_view()


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []

    try:
        result = Result.objects.get(user=request.user)
        if result:
            return redirect(reverse('quiz:user_quiz_detail'))
    except:
        for q in quiz.get_questions():
            answers = []
            for a in q.get_answers():
                ans = {
                    'text': a.text,
                    'uuid': a.uuid,
                    'q_uid': q.uuid
                }
                answers.append(ans)
            questions.append({str(q): answers})
        return JsonResponse({
            'data': questions,
            'time': quiz.time,
        })


class SaveQuiz(LoginRequiredMixin, JsonRequestResponseMixin, View):

    def post(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        print("quiz.title")
        item = self.request_json

        # print(item)
        score = 0
        wrong = 0
        # questions = item['data'].items()
        count = 0
        for x, y in item['data'].items():
            question = Question.objects.get(uuid=x)
            count += 1
            # question = Question.objects.get(uuid=x)
            if y is not None:
                ans = Answer.objects.get(uuid=y)
                if ans.correct:
                    score += 1
                else:
                    wrong += 1

        multipler = 100 / count
        result = score * multipler

        try:
            obj = Result.objects.get(quiz=quiz, user=request.user)
            obj.attempts += 1
            obj.score = round(result)
            obj.save()
        except:
            obj = Result.objects.create(
                quiz=quiz, user=request.user, score=result, attempts=1
            )
            obj.save()

        return self.render_json_response({
            'quiz': str(quiz.category),
            'correct': score,
            'count': count,
            'score': result,
            'not_check': count - score,
            'wrong': wrong
        })


quiz_save = SaveQuiz.as_view()


class FetchApiView(LoginRequiredMixin, JsonRequestResponseMixin, View):

    def post(self, request, pk):
        item = self.request_json

        print(item)

        return self.render_json_response({
            'quiz': 'data send'
        })


# manage views

class ManageDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/manage/dashboard.html'

    def get(self, request):
        result = Result.objects.filter(quiz__module__isnull=True)
        year = result.filter(date__year=datetime.today().strftime('%Y')).count()
        month = result.filter(date__month=datetime.today().strftime('%m')).count()
        day = result.filter(date__day=datetime.today().strftime('%d')).count()
        organizations = Organizations.objects.all()
        print(datetime.today())
        return self.render_to_response({
            'year': year,
            'month': month,
            'day': day,
            'organizations': organizations
        })


manage_dashboard = ManageDashboard.as_view()


class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = 'dashboard/manage/create_quiz.html'
    fields = ['title', 'category', 'number_of_questions', 'score_to_pass', 'time']

    def form_valid(self, form):
        self.object = form.save()
        return redirect('quiz:quiz_detail', pk=self.object.id)


quiz_create_view = QuizCreateView.as_view()


class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ['category', 'number_of_questions', 'score_to_pass', 'time']
    template_name = 'dashboard/manage/quiz_form.html'
    pk_url_kwarg = 'pk'

    # @csrf_exempt
    # def dispatch(self, request, *args, **kwargs):
    #     print('hello world')
    #     return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        object = form.save()
        context = {
            'object': object
        }
        return render(self.request, 'dashboard/manage/quiz_detail.html', context=context)


quiz_update_view = QuizUpdateView.as_view()


def update_quiz(request, pk):
    object = get_object_or_404(Quiz, pk=pk)
    form = QuizForm(instance=object)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=object)
        if form.is_valid():
            object = form.save()
            return render(request, 'dashboard/manage/quiz_detail.html', {'object': object})

    context = {
        'form': form,
        'object': object
    }
    return render(request, 'dashboard/manage/quiz_form.html', context)


@permission_required("quiz.view_quiz")
def active_or_deactive(request, pk):
    object = get_object_or_404(Quiz, pk=pk)
    print(object)
    if object.active:
        object.active = False
    else:
        object.active = True

    object.save()
    return render(request, 'dashboard/manage/active.html', context={'object': object})


class QuizDeleteView(DeleteView):
    model = Quiz
    success_url = reverse_lazy('quiz:quiz_list')
    template_name = 'dashboard/manage/quiz_delete.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            messages.success(self.request, f"hello")
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


quiz_delete_view = QuizDeleteView.as_view()


class QuizListView(ListView):
    model = Quiz
    template_name = 'dashboard/pages/quiz_list.html'
    queryset = Quiz.objects.filter(module=None)


quiz_list_view = QuizListView.as_view()


# htmx detail quiz

class QuizDetailView(TemplateResponseMixin, View):
    template_name = 'dashboard/pages/question_list.html'

    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        questions = quiz.questions.all()
        return self.render_to_response({
            'questions': questions,
            'quiz': quiz
        })

    def post(self, request, quiz_id):
        form = QuestionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save()
            return render(request, 'dashboard/quiz/questions_detail.html', {'object': obj, 'quiz_id': quiz_id})


quiz_detail_view = QuizDetailView.as_view()

from openpyxl import load_workbook


def export_question_excel(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    form = ExportExcelQuestion()
    if request.method.lower() == 'post':
        form = ExportExcelQuestion(files=request.FILES)
        if form.is_valid():
            excel = form.save()
            if excel:
                df = vaex.from_pandas(pd.read_excel(excel.excel_file))

                for x in range(df.length_original()):
                    print(df[x][0])
                    if df[x][0] is not None and df[x][0] != 'nan':
                        obj = Question.objects.create(
                            quiz=quiz,
                            text=df[x][0],
                            uuid=uuid4()
                        )
                        if obj:
                            Answer.objects.bulk_create(
                                [
                                    Answer(question=obj,
                                           text=df[x][1],
                                           uuid=uuid4(), correct=True),
                                    Answer(question=obj,
                                           text=df[x][2],
                                           uuid=uuid4()),
                                    Answer(question=obj,
                                           text=df[x][3],
                                           uuid=uuid4()),
                                    Answer(question=obj,
                                           text=df[x][4],
                                           uuid=uuid4()),
                                ]
                            )

                return HttpResponse('succes')
    context = {
        'form': form,
        'quiz_id': quiz_id
    }
    return render(request, 'dashboard/manage/excel_form.html', context)


def question_form(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    form = QuestionForm(initial={'quiz': quiz})
    formset = answer_formset()

    if request.method == 'POST':

        form = QuestionForm(request.POST)
        formset = answer_formset(request.POST or None)
        if all([form.is_valid(), formset.is_valid()]):
            question = form.save(commit=False)
            quiz_obj = type(form.cleaned_data['quiz'])
            question.save()
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            return render(request, 'dashboard/manage/detail_question.html', {'question': question})

    return render(request, 'dashboard/manage/question_form.html',
                  {'formset': formset, 'form': form, 'quiz_id': quiz_id})


def update_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    formset = answer_formset(instance=question)
    form = QuestionForm(instance=question)
    print(formset)

    if request.method.lower() == 'post':
        form = QuestionForm(request.POST, instance=question)
        formset = answer_formset(request.POST, instance=question)
        print('form=', form.is_valid(), 'formset=', formset.is_valid())
        if all([form.is_valid(), formset.is_valid()]):
            question = form.save(commit=False)
            question.save()
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            return render(request, 'dashboard/manage/detail_question.html', {'question': question})
    context = {
        'formset': formset,
        'form': form,
        'quiz_id': question.quiz.id,
        'question_id': question_id
    }

    return render(request, 'dashboard/manage/question_update_form.html', context)


def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return HttpResponse('')


class HtmxQuizDetailView(DetailView):
    model = Quiz
    template_name = 'dashboard/manage/quiz_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuestionForm()

        return context


htmx_quiz_detail_view = HtmxQuizDetailView.as_view()

# statistics function
import functools


class QuizDashboardCountView(LoginRequiredMixin, CsrfExemptMixin, JsonRequestResponseMixin, View):

    def get(self, request):
        today = datetime.today()
        user_org = self.request.user.organizations
        level_org = user_org.level
        parent_org = None
        # keyingi oy boshi sanasi
        next_month_start = date(datetime.today().year, datetime.today().month + 1, 1)
        next_year_start = date(datetime.today().year + 1, 1, 1)

        prev_month_start = date(datetime.today().year, datetime.today().month, 1)
        prev_year_start = date(datetime.today().year, 1, 1)

        # month = datetime.today().strftime('%m')
        # year = datetime.today().strftime('%Y')
        day = datetime.today().strftime('%d')
        quiz_dmy__next = Quiz.objects.filter(active=True, module__isnull=True).aggregate(
            day=Count('period_date', filter=Q(period_date__day=day)),
            month=Count('period_date', filter=Q(period_date__gte=today) & Q(period_date__lt=next_month_start)),
            year=Count('period_date', filter=Q(period_date__gte=today) & Q(period_date__lt=next_year_start)),
        )

        quiz_dmy__prev = Quiz.objects.filter(active=True, module__isnull=True).aggregate(
            month=Count('period_date', filter=Q(period_date__lt=today) & Q(period_date__gte=prev_month_start)),
            year=Count('period_date', filter=Q(period_date__lt=today) & Q(period_date__gte=prev_year_start)),
        )

        count_users_org = r.zmscore('organization', [x['id'] for x in user_org.get_family().values('id')])
        sum_users_org = functools.reduce(lambda a, b: (0 if a is None else a) + (0 if b is None else b),
                                         count_users_org, 0)

        org_result = r.lrange('organization_result_info', 0, -1)
        data_res = dict()

        for result in org_result:

            result = json.loads(result)
            if request.user.is_superuser:
                parent_org = result['railway']
                if railway := data_res.get(result['railway']):
                    if organization := railway.get(result['organization']):
                        organization.append(result['score'])
                    else:
                        railway[result['organization']] = [result['score']]
                else:
                    data_res[result['railway']] = {
                        result['organization']: [result['score']]
                    }

            if level_org == 0:

                if user_org.organization == result['railway']:
                    parent_org = result['railway']
                    if railway := data_res.get(result['railway']):
                        if organization := railway.get(result['organization']):
                            organization.append(result['score'])
                        else:
                            railway[result['organization']] = [result['score']]
                    else:
                        data_res[result['railway']] = {
                            result['organization']: [result['score']]
                        }
            if level_org == 1:

                if user_org.organization == result['organization']:
                    parent_org = result['organization']
                    if railway := data_res.get(result['organization']):
                        if organization := railway.get(result['organization']):
                            organization.append(result['score'])
                        else:
                            railway[result['department']] = [result['score']]
                    else:
                        data_res[result['organization']] = {
                            result['department']: [result['score']]
                        }
        info_list = []
        score = []
        for key, value in data_res.items():
            keys = value.keys()

            for v in keys:
                avg = [sum(value[v]) / len(value[v]), v]
                info_list.append(avg)
                # bu yerda umumiy organizatsiyalarni ortacha scorelari listga qoshilib boriladi
                score.extend([avg[0]])
        try:

            result = round(sum(score) / len(score))
        except:
            result = 0
        return self.render_json_response({
            'test__next': quiz_dmy__next,
            'test__prev': quiz_dmy__prev,
            'result': result,
            'users': sum_users_org,
            'data_res': info_list,
            'data_name': parent_org
        })


quiz_dashboard_info = QuizDashboardCountView.as_view()


class ResultApiView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request):
        result = json.loads(r.get(f"user:{request.user}:result"))

        return self.render_json_response({
            'data': result.get('data')[-8:],
            'labels': result.get('labels')[-8:]
        })


from django.contrib.auth.decorators import permission_required


class StatisticsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'dashboard/pages/statistics.html'
    permission_required = 'course.view_course'

    def get(self, request):
        print(self.request.user.organizations)
        results = Result.objects.filter(user__organizations__parent__parent__in=[self.request.user.organizations])
        print(results)
        return self.render_to_response({
            'results': results
        })


statistics = StatisticsView.as_view()


class StatisticsOrganizationApi(PermissionRequiredMixin, LoginRequiredMixin, JsonRequestResponseMixin, View):
    permission_required = 'quiz.view_quiz'

    def get(self, request):

        return self.render_json_response({
            'organizations': 'ok'
        })


statistics_org_api = StatisticsOrganizationApi.as_view()


class Employers(TemplateView):
    template_name = 'dashboard/pages/employers.html'

    def get(self, request):
        return self.render_to_response({
            'ok': 'ok'
        })


employers = Employers.as_view()


class OrganizationsView(TemplateView):
    template_name = 'dashboard/pages/organizations.html'

    def get(self, request):
        return self.render_to_response({
            'ok': 'ok'
        })


organizations = OrganizationsView.as_view()
