from rest_framework import serializers
from jobs import models

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Job
        fields = '__all__'

class CandidateAppliedSerializer(serializers.ModelSerializer):

    job = JobSerializer()

    class Meta:
        model = models.CandidateApplied
        fields = ('user', 'resume', 'applied_at', 'job')