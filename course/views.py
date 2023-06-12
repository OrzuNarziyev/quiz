from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import Course, Category, Module, Content, Text
from .forms import CourseForm, ModuleForm, ModuleQuizForm
from quiz.models import Question, Quiz, Result, Answer

from django.forms.models import modelform_factory
from django.apps import apps

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from ckeditor.widgets import CKEditorWidget


class CourseHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'course/course_home.html'

    def get(self, request, slug=None, *args, **kwargs):
        categories = Category.objects.all()
        quiz = None
        if slug is not None:
            cat = Category.objects.get(slug=slug)
            categories = cat.get_children()

        return self.render_to_response({
            'object_list': categories,
            'quiz': quiz
        })


course_home = CourseHomeView.as_view()


class CourseDetail(LoginRequiredMixin, TemplateView):
    template_name = 'course/users/pages/detail.html'

    def get(self, request, pk):
        object = get_object_or_404(Course, pk=pk)
        modules = Module.objects.filter(course=object)
        return self.render_to_response({
            'object': object,
            'modules': modules,
            'count_m':modules.filter(parent__isnull=False).count()
        })

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # try:
    #     #     result = Result.objects.get(user=self.request.user)
    #     # except:
    #     #     result = None
    #     # context['result'] = result
    #     return context


user_course_detail = CourseDetail.as_view()


class CourseListView(TemplateResponseMixin, View):
    template_name = 'course/dashboard/course_list.html'

    # def get(self, request, slug=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if slug is not None:
    #         context['object_list'] = self.get_queryset().filter(
    #             subject__slug=slug)

    #     return self.render_to_response(context)

    def get(self, request):
        object_list = Course.objects.select_related('subject', 'subject__parent').prefetch_related('modules')
        return self.render_to_response({
            'object_list': object_list
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['object_list'] = Course.objects.filter(
                subject__slug=kwargs['slug'])
        except:
            pass

        return context


course_list_view = CourseListView.as_view()


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course/dashboard/manage/course_detail.html'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return super().get_queryset().select_related('subject')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        modules = Module.objects.filter(course=self.object).select_related('parent')
        context['modules'] = modules
        return context


course_detail_view = CourseDetailView.as_view()

from django.utils.text import slugify


class CourseCreateView(CreateView):
    model = Course
    template_name = 'course/dashboard/manage/course_form.html'
    form_class = CourseForm
    success_url = reverse_lazy('course:course_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)


course_create_view = CourseCreateView.as_view()


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'course/dashboard/manage/course_form.html'


course_update_view = CourseUpdateView.as_view()


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'course/dashboard/manage/course_delete.html'
    success_url = reverse_lazy('course:course_list')


course_delete_view = CourseDeleteView.as_view()


class ModuleCreateUpdateView(TemplateResponseMixin, View):
    template_name = 'course/dashboard/manage/module_form.html'

    def get(self, request, course_id=None, module_id=None, *args, **kwargs):
        course = get_object_or_404(Course, pk=course_id)
        if module_id is not None:
            module = get_object_or_404(Module, pk=module_id)
            form = ModuleForm(instance=module)
            return self.render_to_response(
                {'form': form,
                 'course': course
                 }
            )
        else:
            form = ModuleForm(initial={'course': course}, course=course)
            return self.render_to_response(
                {'form': form,
                 'course': course
                 }
            )

    def post(self, request, course_id=None, module_id=None):
        course = get_object_or_404(Course, pk=course_id)
        form = ModuleForm(data=request.POST)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse('course:course_detail', kwargs={'slug': course.slug}))


module_form = ModuleCreateUpdateView.as_view()


class ModuleUpdateView(UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'course/dashboard/manage/module_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        self.object = self.get_object()
        context['course'] = self.object.course
        return context

    def get_success_url(self):
        print(self.object)
        return reverse('course:course_detail', kwargs={'slug': (self.object.course.slug)})


module_update_view = ModuleUpdateView.as_view()


class ModuleDeleteView(DeleteView):
    model = Module
    template_name = 'course/dashboard/manage/module_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.course = self.object.course
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        print(self.course.slug)
        return reverse('course:course_detail', args=(self.course.slug,))


module_delete_view = ModuleDeleteView.as_view()


class ModuleDetailView(TemplateView):
    # model = Module
    template_name = 'course/dashboard/pages/detail_module.html'

    def get(self, request, pk):
        module = get_object_or_404(Module, pk=pk)
        modules = Module.objects.select_related('parent', 'course').filter(course=module.course)

        return self.render_to_response({
            "object": module,
            'modules': modules
        })

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     object = self.get_object()
    #     context['modules'] = Module.objects.prefetch_related('contents__content_type').select_related('course', 'parent').filter(course=object.course)
    #     return context


module_detail = ModuleDetailView.as_view()


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'course/dashboard/manage/content/content-form.html'

    def get_model(self, model_name):
        if model_name in ['video', 'text', 'image', 'file']:
            return apps.get_model(app_label='course', model_name=model_name)

    def get_form(self, model, *args, **kwrags):
        if model is Text:
            Form = modelform_factory(model, exclude=[
                'created',
                'updated',
                'order',
                # 'title'
            ], widgets={'content': CKEditorUploadingWidget()})
        else:
            Form = modelform_factory(model, exclude=[
                'created',
                'updated',
                'order'
            ])

        return Form(*args, **kwrags)

    def dispatch(self, request, module_id, model_name, id=None, *args, **kwargs):
        self.module = get_object_or_404(Module, pk=module_id)
        self.model = self.get_model(model_name)

        if id:
            self.obj = get_object_or_404(self.model, id=id)
        return super().dispatch(request, module_id, model_name, id=None, *args, **kwargs)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj,
                                        'modul_id': module_id,
                                        'model_name': model_name})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                content = Content.objects.create(module=self.module,
                                                 item=obj)
                context = {
                    'item': obj,
                    'module': self.module,
                    'content': content
                }
                return redirect(reverse('course:module_detail', kwargs={'pk': self.module.id}))
                # return render(request, 'course/dashboard/manage/content/content_detail.html', context)
                # return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})


content_create_update_view = ContentCreateUpdateView.as_view()


class ContentDetailView(TemplateResponseMixin, View):
    template_name = 'course/dashboard/manage/content/content-detail.html'

    def get(self, request, module_id, content_id, item_id):
        module = get_object_or_404(Module, id=module_id)
        content = get_object_or_404(Content, id=content_id)
        return self.render_to_response({
            'module': module,
            'content': content
        })


content_detail_view = ContentDetailView.as_view()


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                                  course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user) \
                .update(order=order)
        return self.render_json_response({'saved': 'ok'})


# course quiz block


class ModuleCreateQuiz(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'dashboard/manage/quiz_form.html'

    def get(self, request, module_id, quiz_id=None):
        module = get_object_or_404(Module, pk=module_id)
        course = module.course
        category = module.course.subject
        if quiz_id is not None:
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            form = ModuleQuizForm(request.POST or None, instance=quiz)
            return self.render_to_response({
                'form': form,
                'module': module,
                'object': quiz
            })
        else:
            form = ModuleQuizForm(initial={
                'category': category,
                'course': course,
                'module': module
            })

            return self.render_to_response({
                'form': form,
                'module': module
            })

    def post(self, request, module_id, quiz_id=None):
        module = get_object_or_404(Module, pk=module_id)

        if quiz_id is not None:
            quiz = get_object_or_404(Quiz, pk=quiz_id)
            form = ModuleQuizForm(request.POST or None, instance=quiz)
            if form.is_valid():
                object = form.save()
                return render(request, 'dashboard/manage/quiz_detail.html', {'object': object})
                # return redirect(reverse('course:module_detail', kwargs={'pk': module.id}))
        else:
            form = ModuleQuizForm(request.POST)

            if form.is_valid():

                object = form.save()
                messages.success(request, f'{object} - muvaffaqiyatli saqlandi')
                return redirect(reverse('course:module_detail', kwargs={'pk': module.id}))
            else:
                messages.warning(request, 'form is no valid')
                return redirect(reverse('course:module_detail', kwargs={'pk': module.id}))


module_create_quiz = ModuleCreateQuiz.as_view()


# Users views start

class CourseCategoriesView(LoginRequiredMixin, TemplateView):
    template_name = 'course/users/pages/course_categories.html'

    def get(self, request, slug=None, *args, **kwargs):

        if slug is not None:
            categories = Category.objects.filter(parent__slug=slug)
        else:
            categories = Category.objects.all()

        return self.render_to_response({
            'object_list': categories,
        })


course_categories = CourseCategoriesView.as_view()
