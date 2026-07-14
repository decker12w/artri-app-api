from django.urls import path
from .views import RemedyListCreateView, RemedyDetailView, RemedyIntakeListCreateView, RemedyIntakeDetailView, ExerciseListCreateView, TrainingListCreateView, TrainingReportListCreateView, DailyPainReportListCreateView, UserRegistrationView
from django.urls import path, include

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('remedies/', RemedyListCreateView.as_view(), name='remedy-list-create'),
    path('remedies/<int:pk>/', RemedyDetailView.as_view(), name='remedy-detail'),
    path('remedy-intakes/', RemedyIntakeListCreateView.as_view(), name='remedy-intake-list-create'),
    path('remedy-intakes/<int:pk>/', RemedyIntakeDetailView.as_view(), name='remedy-intake-detail'),
    path('exercises/', ExerciseListCreateView.as_view(), name='exercise-list-create'),
    path('trainings/', TrainingListCreateView.as_view(), name='training-list-create'),
    path('training-reports/', TrainingReportListCreateView.as_view(), name='training-report-list-create'),
    path('daily-pain-reports/', DailyPainReportListCreateView.as_view(), name='daily-pain-report-list-create'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]