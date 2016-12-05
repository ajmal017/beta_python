from django.contrib import admin
from django.contrib.auth.hashers import make_password

from user.models import (SecurityQuestion, SecurityAnswer)


class SecurityQuestionAdmin(admin.ModelAdmin):
    model = SecurityQuestion
    readonly_fields = ('id',)
    list_display = ('id', 'question')

class SecurityAnswerAdmin(admin.ModelAdmin):
    model = SecurityAnswer
    fields=('question', 'answer')
    readonly_fields = ('question',)
    list_display = ('question', 'answer', 'id', 'user_id')

    def get_form(self, request, obj=None, **kwargs):
        form = super(SecurityAnswerAdmin, self).get_form(request, obj, **kwargs)
        def clean_answer(me):
            answer = me.cleaned_data['answer']

            if me.instance:
                if me.instance.answer != answer:
                    answer = make_password(answer.upper())
            else:
                answer = make_password(answer.upper())

            print(answer, "*******************")
            return answer

        form.clean_answer = clean_answer

        return form

    pass

admin.site.register(SecurityQuestion)
admin.site.register(SecurityAnswer, SecurityAnswerAdmin)
