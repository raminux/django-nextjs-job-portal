from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Min, Max, Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from jobs import models
from jobs.serializers import JobSerializer


@api_view(['GET'])
def get_all_jobs(request):
    jobs = models.Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_job_by_id(request, pk):
    job = get_object_or_404(models.Job, pk=pk)
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def add_new_job(request):
    data = request.data

    job = models.Job.objects.create(**data)
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_job(request, pk):
    job = get_object_or_404(models.Job, id=pk)
    
    job.title = request.data['title']
    job.description = request.data['description'] 
    job.email = request.data['email']
    job.address = request.data['address']
    job.job_type = request.data['job_type']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience = request.data['experience']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']

    job.save()
    

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_job(request, pk):
    job = get_object_or_404(models.Job, id=pk)
    job.delete()
    return Response({'message': 'Job is deleted!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_topic_stats(request, topic):
    args = {'title__icontains': topic}
    jobs = models.Job.objects.filter(**args)
    if len(jobs) == 0:
        return Response({'message': 'No stats found for {topic}'.format(topic=topic)})
    
    stats = jobs.aggregate(
        total_jobs=Count('title'),
        avg_positions = Avg('positions'),
        avg_salary = Avg('salary'),
        min_salary = Min('salary'),
        max_salary = Max('salary'),
    )
    return Response(stats)