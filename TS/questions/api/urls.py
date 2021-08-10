from django.urls import path
from django.urls.resolvers import URLPattern

app_name = 'questions'

from questions.api.views import ask_question, all_questions, answer_a_question, all_answers_to_question, vote

urlpatterns = [
    path('ask_question/', ask_question, name="ask_question"),
    path('answer_a_question/', answer_a_question, name="answer_a_question"),
    path('all_questions/', all_questions, name="all_questions"),
    path('all_answers_to_question/', all_answers_to_question, name="all_answers_to_question"),
    path('vote/', vote, name="vote"),
]