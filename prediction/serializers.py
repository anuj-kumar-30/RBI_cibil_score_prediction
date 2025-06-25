from rest_framework import serializers
from .models import PredictionRequest

class PredictionInputSerializer(serializers.Serializer):
    """
    Serializer for validating incoming prediction requests
    This replace's fastapi's pydantic model for request validation
    """
    name = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    monthlyIncome = serializers.IntegerField()
    dataPackExpense = serializers.IntegerField()
    savings = serializers.IntegerField()
    internetUsed = serializers.CharField(max_length=10)
    foodFuelExpensePercent = serializers.CharField(max_length=20)
    hasLoan = serializers.CharField(max_length=10)
    hasLand = serializers.CharField(max_length=10)
    familyMembers = serializers.IntegerField()
    childrenCount = serializers.IntegerField()
    childrenStatus = serializers.CharField(max_length=50)
    cookingTogether = serializers.CharField(max_length=10)
    earningMembers = serializers.IntegerField()
    dependentMembers = serializers.IntegerField()
    lpgRefillFrequency = serializers.CharField(max_length=20)
    lpgPreference = serializers.CharField(max_length=50)
    lpgChallenges = serializers.CharField(max_length=100)
    cylinderPreference = serializers.CharField(max_length=100)
    jobType = serializers.CharField(max_length=100)
    emergencyFundSource = serializers.CharField(max_length=50)
    facedEmergency = serializers.CharField(max_length=10)
    assets = serializers.CharField(max_length=100)
    ownsVehicle = serializers.CharField(max_length=100)
    incomeCycle = serializers.CharField(max_length=50)
    awareOfGovtScheme = serializers.CharField(max_length=10)
    pastLoanDefault = serializers.CharField(max_length=10)

class PredictionOutputSerializer(serializers.Serializer):
    """
    Serializer for prediction response
    this ensures consistent API response format
    """
    score = serializers.FloatField()
    risk_category = serializers.CharField(max_length=20)

class PredictionRequestSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for database operations
    automatically generates fields based on the model
    """
    class Meta:
        model = PredictionRequest
        fields = '__all__'