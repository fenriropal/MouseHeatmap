from django.urls import path

from . import views

app_name = 'mouseheatmapapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('read_minmax/', views.ReadMinMaxView.read, name='read_minmax'),
    # path(url(r'^gen_durationtimehm/(?P<value>\d+)/$'), views.GenDurationTimeHMView.as_view(), name='gen_durationtimehm'),
    path('gen_mousemovementhm/<int:use_value>/', views.GenMouseMovementHMView.as_view(), name='gen_mousemovementhm'),
    path('gen_durationtimehm/<int:use_value>/', views.GenDurationTimeHMView.as_view(), name='gen_durationtimehm'),
    path('gen_mouseclickhm/<int:use_value>/', views.GenMouseClickHMView.as_view(), name='gen_mouseclickhm'),
    path("get_path/", views.
    getpath, name="get_path"),
]