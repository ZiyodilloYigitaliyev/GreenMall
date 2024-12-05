import boto3
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, ProductMedia
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404

class ProductListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  
        return [IsAuthenticated()]  

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
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
                s3_path = f"product_media/{file.name}"  # S3 ichidagi papka va fayl nomi
                s3_client.upload_fileobj(
                    file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    s3_path,
                    ExtraArgs={'ContentType': file.content_type, 'ACL': 'public-read'}  # Public URL uchun
                )

                # S3'da yuklangan fayl URL'si
                s3_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{s3_path}"

                # Fayl ma'lumotini saqlash
                ProductMedia.objects.create(product=product, file_url=s3_url)  # 'file' maydoni 'file_url' bo'lishi kerak

            # Return updated serializer data
            updated_serializer = ProductSerializer(product)  # If you want to return updated data
            return Response(updated_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
