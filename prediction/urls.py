from django.urls import path
from .views import PredictAPIView, health_check, PredictionHistoryAPIView, prediction_form, history_page, landing_page

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('predict/', PredictAPIView.as_view(), name='predict'),
    path('health/', health_check, name='health_check'),
    path('api/history/', PredictionHistoryAPIView.as_view(), name='prediction_history'),
    path('history/', history_page, name='history_page'),
    path('predict-form/', prediction_form, name='prediction_form'),
]