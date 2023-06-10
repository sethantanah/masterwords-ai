from django.urls import path

from .views.contentviews import home_page, generate_post, generate_post_ideas, word_tuner
from .views.converters import UploadPDFView, download_word

urlpatterns = [
path('', home_page, name='home_page')
]

urlpatterns +=[
    path('post-ideas', generate_post_ideas, name='post_ideas'),
    path('post-ideas/<str:idea>', generate_post, name='gen_post'),
    path('word-tuners', word_tuner, name='word_tuners'),
    path('pdf2word', UploadPDFView.as_view(), name='pdf2word'),
    path('download_docx', download_word, name='download_docx'),

]