from django.contrib import admin
from .models import *

admin.site.register(Person)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(Survey)
admin.site.register(GivenAnswer)
