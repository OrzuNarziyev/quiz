from django.contrib import admin
from .models import Quiz, Question, Answer, Result, Category, ExcelFileUploaded
# Register your models here.
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin, TreeRelatedFieldListFilter


# admin.site.register(
#     Category,
#     DraggableMPTTAdmin,
#     list_display=(
#         'name',
#         # ...more fields if you feel like it...
#     ),
#     list_display_links=(
#         'name',
#     ),
# )

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 50
    # list_display = ['tree_actions', 'name']
    # list_display_links = ['name']
    prepopulated_fields = {'slug': ('name', 'parent')}
    mptt_indent_field = "name"
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    mptt_level_indent = 50
    list_display = ['category', 'module', 'title', 'created', 'active']
    list_editable = ['active']
    list_filter = (
        ('category', TreeRelatedFieldListFilter),
    )


class InlineAnswer(admin.TabularInline):
    model = Answer


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['order', 'question', 'text', 'correct']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['order', 'quiz', 'text', 'created']
    inlines = [InlineAnswer, ]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'user', 'score', 'attempts', 'date', 'update_date']


@admin.register(ExcelFileUploaded)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['excel_file']


dict = {
    "Aloqa va signallashtirish": [
        "Aloqa",
        "Signallashtirish(СЦБ)"
    ],
    "Elektr xo'jaligi": [
        "Elektromantyor",
        "Elektromexanik",
        "Katta Elektromantyor"
        "Katta Elektrmexanik",
        "Kontakt elektr tarmoqlari bo'limi boshlig'i",
        "Tuman elektr tarmoqlari bo'limi boshlig'i",
        "Tortuv nim stansiya boshlig'i",
        "Boshliq o'rinbosari"
    ],

    "Tashish va bekat ishlari": [
        'Poezd tuzuvchisi',
        'Bekat navbatchisi',
        "Bekat boshlig'ining o'rinbosari",
        "Bekat boshlig'i"
    ],
    "Yuk va tijorat ishlari": [
        "Yuk qabul qiluvchi topshiruvchi",
        "Katta yuk qabul qiluvchi topshiruvchi",
        "Yuk xazinasichi",
        "Katta yuk xazinachisi"
    ],
    "Yo'l xo'jaligi": [
        "Brigadir",
        "Katta yo'l ustasi",
        "Temir yo'l masofasi boshlig'i o'rinbosari",
        "Yo'l tamirlovchi",
        "Yo'l ustasi",
    ],
    "Lokomativ xo'jaligi": [
        "Eksplutatsiya",
        "Tamirlash"
    ],
    "Vagon xo'jaligi": [
        "Eksplutatsiya-20",
        "Tamirlash-20"
    ],

}

# Tashish va bekat ishlari,
# Bekat boshlig'i,
# Bekat boshlig'ining o'rinbosari,
# Bekat navbatchisi,
# Poezd tuzuvchisi,
#
#
# Yuk va tijorat ishlari,
# Katta yuk qabul qiluvchi topshiruvchi,
# Katta yuk xazinachisi,
# Yuk qabul qiluvchi topshiruvchi,
# Yuk xazinasichi]
#


# Aloqa va signallashtirish
# Aloqa
# Signallashtirish(СЦБ)
# Elektr xo'jaligi


# ...: Elektromantyor
#     ...: Elektromexanik
#     ...: Katta Elektrmexanik
#     ...: Katta Elektromantyor
#     ...: Tashish va bekat ishlari
#     ...: Lokomativ xo'jaligi
#     ...: Eksplutatsiya
#     ...: Tamirlash
#     ...: Tashish va bekat ishlari
#     ...: Bekat boshlig'i
#     ...: Bekat boshlig'ining o'rinbosari
#     ...: Bekat navbatchisi
#     ...: Poezd tuzuvchisi
#     ...: Vagon xo'jaligi
#     ...: Eksplutatsiya-20
#     ...: Tamirlash-20
#     ...: Yo'l xo'jaligi
#     ...: Brigadir
#     ...: Katta yo'l ustasi
#     ...: Temir yo'l masofasi boshlig'i o'rinbosari
#     ...: Yo'l tamirlovchi
#     ...: Yo'l ustasi
#     ...: Yuk va tijorat ishlari
#     ...: Katta yuk qabul qiluvchi topshiruvchi
#     ...: Katta yuk xazinachisi
#     ...: Yuk qabul qiluvchi topshiruvchi
#     ...: Yuk xazinasichi
