import boto3
import graphene
from graphene_django.types import DjangoObjectType
from .models import Task, UserImage  # Import models from models.py
from django.conf import settings
from django.contrib.auth.models import User
from graphql import GraphQLError
from rest_framework.permissions import IsAuthenticated
from graphene_django.types import DjangoObjectType

# Define a Task type for GraphQL
class TaskType(DjangoObjectType):
    class Meta:
        model = Task

# Define a User type for GraphQL
class UserType(DjangoObjectType):
    class Meta:
        model = User

# Create a Query class that returns all tasks
class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()

# Mutation for registering a new user
class Register(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return Register(user=user)

# Mutation for uploading images to S3

import base64
from io import BytesIO
from django.core.files.base import ContentFile

class UploadImage(graphene.Mutation):
    success = graphene.Boolean()
    image_url = graphene.String()

    class Arguments:
        image = graphene.String(required=True)

    def mutate(self, info, image):
        user = info.context.user

        if not user.is_authenticated:
            raise GraphQLError('Authentication credentials were not provided.')

        # Proceed with your logic
        file_name = f"{user.username}_uploaded_image.jpg"
        image_data = ContentFile(base64.b64decode(image), name=file_name)

        # Save image to user profile (assuming UserImage model)
        user_image = UserImage(user=user, image_url=image_data)
        user_image.save()

        return UploadImage(success=True, image_url=user_image.image_url)

# Combine all mutations
class Mutation(graphene.ObjectType):
    register = Register.Field()
    upload_image = UploadImage.Field()

# Define the schema with both Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
