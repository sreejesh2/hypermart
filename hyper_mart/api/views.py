from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import User,Category,Product
from .serializers import UserSerializer,CategorySerializer,ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
# Create your views here.
from rest_framework.permissions import IsAuthenticated

class UserCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active = True)
            return Response({"message":"registration success","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

current_user = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'status': 0, 'message': 'Invalid phone or password'}, status=400)

        if user.check_password(password):
            

            refresh = RefreshToken.for_user(user)

            response_data = {
                'status': 1,
                'data': {
                    'token': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    'user': {
                        'id': user.id,
                        'full_name': user.full_name,
                        'phone': user.phone,
                        'dob': user.dob,
                        'email': user.email,
                        'gender': user.gender,
                        'user_type': user.user_type,
                        'is_active': user.is_active
                    }
                }
            }

          
            return Response(response_data)

        return Response({'status': 0, 'message': 'Invalid phone or password'}, status=400)

 
class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            serializer = CategorySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data, "status": 1, "message": "Category created"}, status=status.HTTP_201_CREATED)

            return Response({"status": 0, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status": 0, "message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Response({"status": 0, "message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"status": 1, "message": "Category updated", "data": serializer.data})

        return Response({"status": 0, "message": "Invalid data", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)    


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({"status": 1, "message": "Category list", "data": serializer.data})
        
        except Exception as e:
            return Response({"status": 0, "message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        

class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def delete(self, request, pk, *args, **kwargs):
        category = self.get_object(pk)

        if category is not None:
            category.delete()
            return Response({"status": 1, "message": "Category deleted"})

        return Response({"status": 0, "message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)      
    
class ProductCreateView(APIView):
    def post(self, request, category_id, format=None):
        try:
            category = Category.objects.get(id=category_id)
            request.data['category'] = category.id  # Assign the category ID to the product data

            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Product created successfully',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Validation error',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Category not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred while creating the product',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProductUpdateView(APIView):
    def put(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'message': 'Product updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Validation error',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Product not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'An error occurred while updating the product',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        \
            

class ProductListView(APIView):
    def get(self, request, category_id, format=None):
        try:
            category = Category.objects.get(id = category_id)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)

            return Response({
                'status': 'success',
                'message': f'Products under category {category_id} retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An error occurred while retrieving products under category {category_id}',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
        


class ProductDetailView(APIView):
    def get(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)

            return Response({
                'status': 'success',
                'message': f'Product {pk} retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': f'Product {pk} not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An error occurred while retrieving product {pk}',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
        

class ProductDeleteView(APIView):
    def delete(self, request, pk, format=None):
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({
                'status': 'success',
                'message': f'Product {pk} deleted successfully',
                'data': None
            }, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({
                'status': 'error',
                'message': f'Product {pk} not found',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'An error occurred while deleting product {pk}',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        