from django.urls import path


from subjects import views

app_name = 'subjects'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:subject_id>', views.index, name='detail'),
    path('paper/<int:paper_id>/', views.paper_view, name='paper'),

    path('autosuggest/', views.autosuggest, name="autosuggest")
]
