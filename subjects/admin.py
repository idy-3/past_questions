from django.contrib import admin

from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError

from django.forms import inlineformset_factory

from subjects.models import Subject, Paper, Question, Choice

admin.site.site_header = "Naija Expo Admin"
admin.site.site_title = "Naija Expo Admin Area"
admin.site.index_title = "Welcome to the Naija Expo admin area!"


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


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['instruction']}),
                 (None, {'fields': ['question']}),
                 (None, {'fields': ['paper']}),
                 (None, {'fields': ['description']}),
                 ('Image', {'fields': ['image'], 'classes': ['collapse']})]
    inlines = [ChoiceInline]
    list_display = ['question', 'paper']
    list_filter = ('paper',)


class PaperAdmin(admin.ModelAdmin):
    list_filter = ('subject', 'exam_year')
    list_display = ('subject', 'exam_year')


class SubjectAdmin(admin.ModelAdmin):
    list_filter = ('name', 'exam_type')
    list_display = ('name', 'exam_type')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Paper, PaperAdmin)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
