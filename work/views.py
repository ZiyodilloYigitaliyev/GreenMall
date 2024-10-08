from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Project, ProjectMedia
from .serializers import ProjectSerializer
from django.shortcuts import get_object_or_404


class ProjectListCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # Supports file uploads

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # No authentication required for GET requests
        return [IsAuthenticated()]  # Authentication required for POST, PUT, DELETE requests

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save()  # Save project first

            # Handle media files
            media_files = request.FILES.getlist('media')  # Retrieve media files
            for file in media_files:
                ProjectMedia.objects.create(project=project, file=file)  # Create ProjectMedia instances

            # Return updated serializer data
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
