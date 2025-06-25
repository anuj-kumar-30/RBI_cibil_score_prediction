from django.db import models

# Create your models here.
class PredictionRequest(models.Model):
    """
    Model to store prediction requests and results
    This replaces the in-memory storage that FastAPI might use
    """
    # Basic Info
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    # finacial info
    monthlyIncome = models.IntegerField()
    dataPackExpense = models.IntegerField()
    savings = models.IntegerField()

    # usage info
    internetUsed = models.CharField(max_length=10) #y/n
    foodFuelExpensePercent = models.CharField(max_length=20)
    hasLoan = models.CharField(max_length=10) #y/n
    hasLand = models.CharField(max_length=10) # y/n

    # family info
    familyMembers = models.IntegerField()
    childrenCount = models.IntegerField()
    childrenStatus = models.CharField(max_length=50)
    cookingTogether = models.CharField(max_length=10)
    earningMembers = models.IntegerField()
    dependentMembers = models.IntegerField()

    # LPG info
    lpgRefillFrequency = models.CharField(max_length=20)
    lpgPreference = models.CharField(max_length=50)
    lpgChallenges = models.CharField(max_length=100)
    cylinderPreference = models.CharField(max_length=100)

    # other info
    jobType = models.CharField(max_length=100)
    emergencyFundSource = models.CharField(max_length=50)
    facedEmergency = models.CharField(max_length=10) # y/n
    assets = models.CharField(max_length=100)
    ownsVehicle = models.CharField(max_length=100)
    incomeCycle = models.CharField(max_length=50)
    awareOfGovtScheme = models.CharField(max_length=10) #y/n
    pastLoanDefault = models.CharField(max_length=10) #y/n

    # prediction results
    score = models.FloatField(null=True, blank=True)
    risk_category = models.CharField(max_length=20, null=True, blank=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prediction_requests'

    def __str__(self):
        return f"{self.name} --> {self.risk_category}"
