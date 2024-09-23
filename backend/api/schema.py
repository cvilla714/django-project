import boto3
import graphene
from graphene_django.types import DjangoObjectType
from .models import Task, UserImage
from django.conf import settings
from django.contrib.auth.models import User
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from graphql_jwt.utils import jwt_decode
import graphql_jwt
import base64
from django.core.files.base import ContentFile

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
class UploadImage(graphene.Mutation):
    success = graphene.Boolean()
    image_url = graphene.String()

    class Arguments:
        image = graphene.String(required=True)

    def mutate(self, info, image):
        auth = info.context.META.get('HTTP_AUTHORIZATION')
        if not auth:
            raise GraphQLError("Authentication credentials were not provided.")
        
        # Extract token and decode manually
        token = auth.split(" ")[1]  # Assuming 'Bearer <token>'
        payload = jwt_decode(token)
        
        # Print payload to see what fields it contains
        print(f"Decoded JWT payload: {payload}")

        # If user_id is not in payload, change to 'user_id' to 'user' or 'username' depending on the payload structure
        # user_id = payload.get('user_id')  # Modify this line based on actual payload
        # if not user_id:
            # raise GraphQLError("User ID not found in the token payload.")

        username = payload.get('username')
        if not username:
            raise GraphQLError("Username not found in the token payload.")
        
        user = User.objects.get(username=username)
        print(f"User: {user}")

        # Proceed with the rest of the logic
        file_name = f"{user.username}_uploaded_image.jpg"
        image_data = ContentFile(base64.b64decode(image), name=file_name)
        user_image = UserImage(user=user, image_url=image_data)
        user_image.save()

        return UploadImage(success=True, image_url=user_image.image_url)

# Combine all mutations
class Mutation(graphene.ObjectType):
    register = Register.Field()
    upload_image = UploadImage.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

# Define the schema with both Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
