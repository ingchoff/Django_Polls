from django.contrib import admin
from django.contrib.auth.models import Permission

from polls.models import Poll, Question, Choice, Comment

admin.site.register(Permission)

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2
    classes = ['collapse']


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
    classes = ['collapse']


class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date', 'del_flag']
    list_per_page = 10

    list_filter = ['start_date', 'end_date', 'del_flag', 'title']
    search_fields = ['title']

    fieldsets = [
        (None, {'fields': ['title', 'del_flag']}),
        ("Duration", {'fields': ['start_date', 'end_date'], 'classes': ['collapse']})
    ]

    inlines = [QuestionInline]


admin.site.register(Poll, PollAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'text']
    list_per_page = 10

    list_filter = ['poll']
    search_fields = ['poll__title']

    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'value']
    list_per_page = 15

    list_filter = ['question', 'text', 'value']
    search_fields = ['question__text']


admin.site.register(Choice, ChoiceAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'title', 'email', 'tel']


admin.site.register(Comment, CommentAdmin)
