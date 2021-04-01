from django.contrib import admin

from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from subjects.models import Subject, Paper, Question, Choice

admin.site.site_header = "Naija Revisions Admin"
admin.site.site_title = "Naija Revisions Admin Area"
admin.site.index_title = "Welcome to the Naija Revisions admin area!"

# IMPORT EXPORT RESOURCE CLASSES


class SubjectResource(resources.ModelResource):

    class Meta:
        model = Subject


class PaperResource(resources.ModelResource):

    class Meta:
        model = Paper


class QuestionResource(resources.ModelResource):

    class Meta:
        model = Question


class ChoiceResource(resources.ModelResource):

    class Meta:
        model = Choice

# MODEL ADMIN CLASSES


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        # custom validation across forms in the formset
        count = 0
        for form in self.forms:
            try:
                # print(form.cleaned_data)
                if form.cleaned_data.get('is_correct'):
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise ValidationError('You must specify the correct answer.')


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    max_num = 5
    formset = ChoiceInlineFormSet


class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    fieldsets = [(None, {'fields': ['instruction']}),
                 (None, {'fields': ['question']}),
                 (None, {'fields': ['paper']}),
                 (None, {'fields': ['description']}),
                 ('Image', {'fields': ['image'], 'classes': ['collapse']})]
    inlines = [ChoiceInline]
    list_display = ['question', 'paper']
    list_filter = ('paper',)


class PaperAdmin(ImportExportModelAdmin):
    resource_class = PaperResource
    list_filter = ('subject', 'exam_year')
    list_display = ('subject', 'exam_year')


class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    list_filter = ('name', 'exam_type')
    list_display = ('name', 'exam_type')


class ChoiceAdmin(ImportExportModelAdmin):
    resource_class = ChoiceResource


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
