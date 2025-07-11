# Generated by Django 5.2.3 on 2025-06-25 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PredictionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('monthly_income', models.IntegerField()),
                ('data_pack_expense', models.IntegerField()),
                ('savings', models.IntegerField()),
                ('internet_used', models.CharField(max_length=10)),
                ('food_fuel_expense_percent', models.CharField(max_length=20)),
                ('family_members', models.IntegerField()),
                ('children_count', models.IntegerField()),
                ('children_status', models.CharField(max_length=50)),
                ('cooking_together', models.CharField(max_length=10)),
                ('earning_members', models.IntegerField()),
                ('dependent_members', models.IntegerField()),
                ('lpg_refill_frequency', models.CharField(max_length=20)),
                ('lpg_preference', models.CharField(max_length=50)),
                ('lpg_challenges', models.CharField(max_length=100)),
                ('cylinder_preferences', models.CharField(max_length=100)),
                ('job_type', models.CharField(max_length=100)),
                ('emergency_fund_source', models.CharField(max_length=50)),
                ('faced_emergency', models.CharField(max_length=10)),
                ('assests', models.CharField(max_length=100)),
                ('has_loan', models.CharField(max_length=10)),
                ('owns_vechile', models.CharField(max_length=100)),
                ('income_cycle', models.CharField(max_length=50)),
                ('aware_of_govt_scheme', models.CharField(max_length=10)),
                ('past_loan_default', models.CharField(max_length=10)),
                ('score', models.FloatField(blank=True, null=True)),
                ('risk_category', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'prediction_requests',
            },
        ),
    ]
