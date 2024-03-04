
from rest_framework import serializers
from .models import User,Category,Product

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'password', 'dob', 'email', 'gender', 'user_type', 'is_active','is_staff')
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password) 
        instance.save()
        return instance    
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nest the CategorySerializer for the ForeignKey relationship

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'description', 'price', 'offerprice', 'quantity', 'is_out_of_stock', 'qr_code', 'image')    