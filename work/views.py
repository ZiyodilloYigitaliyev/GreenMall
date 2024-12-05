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

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save()  # Save the product and get the instance
                media_files = request.FILES.getlist('media')  # Retrieve media files

                # S3 bucket sozlamalari
                s3_client = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_REGION_NAME
                )

                for file in media_files:
                    # S3'ga fayl yuklash
                    s3_path = f"project_media/{file.name}"  # S3 ichidagi papka va fayl nomi
                    s3_client.upload_fileobj(
                        file,
                        settings.AWS_STORAGE_BUCKET_NAME,
                        s3_path,
                        ExtraArgs={'ContentType': file.content_type, 'ACL': 'public-read'}  # Public URL uchun
                    )

                    # S3'da yuklangan fayl URL'si
                    s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_path}"

                    # Fayl ma'lumotini saqlash
                    ProjectMedia.objects.create(product=product, file_url=s3_url)  # 'file' maydoni 'file_url' bo'lishi kerak

                # Return updated serializer data
                updated_serializer = ProjectSerializer(product)  # If you want to return updated data
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
