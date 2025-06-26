from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import (
    PredictionInputSerializer,
    PredictionOutputSerializer,
    PredictionRequestSerializer,
)
from .services import ml_service
from .models import PredictionRequest

# Create your views here.
class PredictAPIView(APIView):
    """
    API view for making predictions
    This replace our fastapi endpoint function
    """
    def post(self, request):
        """
        Handle POST requests for predictions
        similar to fastapi's @app.post('/predict') function
        """
        try:
            # validate input data using serializer
            input_serializer = PredictionInputSerializer(data = request.data)
            if not input_serializer.is_valid():
                return Response(
                    {'error':"Invalid Input data", 'details':input_serializer.errors},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            # GET validated data
            validated_data = input_serializer.validated_data

            # make prediction using ml_service
            prediction_result = ml_service.predict(validated_data)

            # save to database
            self.save_prediction_request(validated_data, prediction_result)

            # return prediction result
            output_serializer = PredictionOutputSerializer(data=prediction_result)

            if output_serializer.is_valid():
                return Response(output_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'prediction Serialization failed'},
                    status = status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return Response(
                {'error':str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def save_prediction_request(self, input_data, prediction_result):
        """
        Save prediction request to database for audit trail
        This is additional functionality not in FastAPI version
        """
        try:
            model_data = {
                'name': input_data.get('name'),
                'state': input_data.get('state'),
                'city': input_data.get('city'),
                'monthlyIncome': input_data.get('monthlyIncome'),
                'internetUsed': input_data.get('internetUsed'),
                'dataPackExpense': input_data.get('dataPackExpense'),
                'foodFuelExpensePercent': input_data.get('foodFuelExpensePercent'),
                'hasLoan': input_data.get('hasLoan'),
                'familyMembers': input_data.get('familyMembers'),
                'childrenCount': input_data.get('childrenCount'),
                'childrenStatus': input_data.get('childrenStatus'),
                'cookingTogether': input_data.get('cookingTogether'),
                'lpgRefillFrequency': input_data.get('lpgRefillFrequency'),
                'earningMembers': input_data.get('earningMembers'),
                'dependentMembers': input_data.get('dependentMembers'),
                'jobType': input_data.get('jobType'),
                'emergencyFundSource': input_data.get('emergencyFundSource'),
                'facedEmergency': input_data.get('facedEmergency'),
                'assets': input_data.get('assets'),
                'ownsVehicle': input_data.get('ownsVehicle'),
                'incomeCycle': input_data.get('incomeCycle'),
                'savings': input_data.get('savings'),
                'awareOfGovtScheme': input_data.get('awareOfGovtScheme'),
                'pastLoanDefault': input_data.get('pastLoanDefault'),
                'lpgPreference': input_data.get('lpgPreference'),
                'lpgChallenges': input_data.get('lpgChallenges'),
                'cylinderPreference': input_data.get('cylinderPreference'),
                'score': prediction_result.get('score'),
                'risk_category': prediction_result.get('risk_category'),
                'hasLand': input_data.get('hasLand'),
            }
            
            PredictionRequest.objects.create(**model_data)
            
        except Exception as e:
            # Log error but don't fail the prediction
            print(f"Failed to save prediction request: {str(e)}")

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint
    similar to fastapi's health check
    """
    return Response(
        {'status':'healthy'},
        status=status.HTTP_200_OK
    )
class PredictionHistoryAPIView(APIView):
    """
    API view for getting prediction history
    additional functionality not in fastapi version
    """
    def get(self, request):
        """GET all prediction history"""
        try:
            predictions = PredictionRequest.objects.all().order_by('-created_at')
            serializer = PredictionRequestSerializer(predictions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return "Unable to get the prediction results"

def prediction_form(request):
    if request.method == 'POST':
        # Collect form data and send to API
        import requests
        api_url = 'https://rbicibilscoreprediction-production.up.railway.app/api/predict/'  # Use Railway deployment URL
        data = request.POST.dict()
        
        # First, let's check if the service is alive
        try:
            health_check_url = 'https://rbicibilscoreprediction-production.up.railway.app/api/health/'
            health_response = requests.get(health_check_url, timeout=10)
            health_status = f"Health check: {health_response.status_code}"
        except Exception as health_error:
            health_status = f"Health check failed: {str(health_error)}"
        
        try:
            response = requests.post(api_url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return render(request, 'prediction/predict_form.html', {
                    'result': result, 
                    'data': data,
                    'success': True,
                    'health_status': health_status
                })
            else:
                # Handle API errors
                error_message = f"API Error: Status {response.status_code}"
                try:
                    error_data = response.json()
                    error_message += f" - {error_data.get('error', 'Unknown error')}"
                except:
                    error_message += f" - {response.text}"
                
                return render(request, 'prediction/predict_form.html', {
                    'error': error_message,
                    'data': data,
                    'success': False,
                    'health_status': health_status
                })
                
        except requests.exceptions.Timeout as e:
            # Handle timeout specifically
            return render(request, 'prediction/predict_form.html', {
                'error': f"Timeout Error: The API took too long to respond. This might be because the Railway service is sleeping (free tier limitation). Please try again in a few seconds. Error: {str(e)}",
                'data': data,
                'success': False,
                'health_status': health_status
            })
        except requests.exceptions.RequestException as e:
            # Handle connection errors
            return render(request, 'prediction/predict_form.html', {
                'error': f"Connection Error: {str(e)}. The Railway service might be down or restarting. Please try again later.",
                'data': data,
                'success': False,
                'health_status': health_status
            })
        except Exception as e:
            # Handle other errors
            return render(request, 'prediction/predict_form.html', {
                'error': f"Unexpected Error: {str(e)}",
                'data': data,
                'success': False,
                'health_status': health_status
            })
    
    return render(request, 'prediction/predict_form.html')

def history_page(request):
    return render(request, 'prediction/history.html')

def landing_page(request):
    return render(request, 'prediction/landing.html')