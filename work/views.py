import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Project, ProjectMedia
from .serializers import ProjectSerializer


class ProjectListCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Fayl yuklash uchun parser

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET uchun autentifikatsiya talab qilinmaydi
        return [IsAuthenticated()]  # POST, PUT, DELETE uchun autentifikatsiya talab qilinadi

    def upload_to_s3(self, file):
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        file_name = f'project_media/{file.name}'
        try:
            s3.upload_fileobj(file, bucket_name, file_name, ExtraArgs={'ACL': 'public-read'})
            file_url = f'https://{bucket_name}.s3.amazonaws.com/{file_name}'
            return file_url
        except Exception as e:
            raise Exception(f"Error uploading file to S3: {str(e)}")

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()  # Loyihani saqlash

            # Fayllarni S3'ga yuklash
            media_files = request.FILES.getlist('media')  # Fayllarni olish
            for file in media_files:
                file_url = self.upload_to_s3(file)  # S3'ga yuklash
                ProjectMedia.objects.create(project=project, file_url=file_url)  # Fayl URL'sini saqlash

            updated_serializer = ProjectSerializer(project)
            return Response(updated_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
