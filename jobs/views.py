from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Min, Max, Count
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from jobs import models
from jobs.serializers import JobSerializer, CandidateAppliedSerializer
from jobs import filters


@api_view(['GET'])
def get_all_jobs(request):
    
    filterset = filters.JobsFilter(
        request.GET, 
        queryset=models.Job.objects.all().order_by('id')
        )
    
    # Pagination
    result_per_page = 3
    counts = filterset.qs.count()
    paginator = PageNumberPagination()
    paginator.page_size = result_per_page

    queryset = paginator.paginate_queryset(filterset.qs, request)
    print(f'paginator: {vars(paginator.page)}')
    serializer = JobSerializer(queryset, many=True)
    return Response({
        "page": paginator.page.number,
        "counts": counts,
        'result_per_page': result_per_page,
        'jobs': serializer.data

    })


@api_view(['GET'])
def get_job_by_id(request, pk):
    job = get_object_or_404(models.Job, pk=pk)

    candidates = job.candidateapplied_set.all().count()

    serializer = JobSerializer(job, many=False)
    return Response({'job': serializer.data, 'candidates': candidates})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_new_job(request):
    request.data['user'] = request.user
    data = request.data

    job = models.Job.objects.create(**data)
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request, pk):
    
    job = get_object_or_404(models.Job, id=pk)
    if job.user != request.user:
        return Response({'message': 'You can not update this job'}, status=status.HTTP_403_FORBIDDEN)
        
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
@permission_classes([IsAuthenticated])
def delete_job(request, pk):
    job = get_object_or_404(models.Job, id=pk)
    if job.user != request.user:
        return Response({'message': 'You can not update this job'}, status=status.HTTP_403_FORBIDDEN)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_job(request, pk):
    user = request.user
    job = get_object_or_404(models.Job, id=pk)
    if user.userprofile.resume == '':
        return Response({'error': 'Please upload your resume first'}, status=status.HTTP_400_BAD_REQUEST)
    
    if job.last_apply_date < timezone.now():
        return Response({'error': 'You can not apply to this job. Date is over!'}, status=status.HTTP_400_BAD_REQUEST)

    # Instead of using related_name argument when defining the CandidateApplied model, we can use 
    # candidateapplied_set method to access the mentiond field from the job class. 
    already_applied = job.candidateapplied_set.filter(user=user).exists()
    if already_applied:
        return Response({'error': 'You have already applied to this job.', }, status=status.HTTP_400_BAD_REQUEST)
    
    job_applied = models.CandidateApplied.objects.create(
        job=job, 
        user=user,
        resume=user.userprofile.resume
    )

    return Response({'applied': True, 'job_id': job_applied.id}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_applied_jobs(request):
    args = {'user_id': request.user.id}

    jobs = models.CandidateApplied.objects.filter(**args)
    serializer = CandidateAppliedSerializer(jobs, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_applied(request, pk):
    user = request.user
    job = get_object_or_404(models.Job, id=pk)

    applied = job.candidateapplied_set.filter(user=user).exists()

    return Response(applied)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_posted_jobs(request):

    args = {'user': request.user.id}
    jobs = models.Job.objects.filter(**args)
    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def candidates_applied(request, pk):
    user = request.user
    job = get_object_or_404(models.Job, id=pk)
    if job.user != user:
        return Response({'error': 'You can not see this job applicants!'}, status=status.HTTP_403_FORBIDDEN)
    
    candidates = job.candidateapplied_set.all()
    serializer = CandidateAppliedSerializer(candidates, many=True)
    return Response(serializer.data)