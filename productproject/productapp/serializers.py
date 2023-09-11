from rest_framework import serializers
from .models import Orders, Product
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],

        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  
    def create(self, validated_data):
            print("serialiser called")
            value=validated_data['name']
            existing_product = Product.objects.filter(name__iexact=value).first()

            if existing_product:
                raise serializers.ValidationError("A product with this name already exists.")
            product = Product.objects.create(**validated_data)
            return product
        

class OrdersSerializer(serializers.ModelSerializer):
    products=ProductSerializer(many=True)
    class Meta:
        model = Orders
        fields = '__all__'
    def create(self, validated_data):
        products_data = validated_data.pop('products')
        
        order = Orders.objects.create(**validated_data)
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            order.products.add(product)
        
        return order
