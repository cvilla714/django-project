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
import uuid

# Initialize the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'  # Update with your S3 region if needed
)
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
        
        token = auth.split(" ")[1]
        payload = jwt_decode(token)
        print(f"Decoded JWT payload: {payload}")
        
        username = payload.get('username')
        if not username:
            raise GraphQLError("Username not found in the token payload.")
        
        user = User.objects.get(username=username)
        print(f"User: {user}")

        # Generate a unique filename using a UUID and the username
        unique_filename = f"user_images/{user.username}_uploaded_image_{uuid.uuid4()}.jpg"
        image_data = ContentFile(base64.b64decode(image), name=unique_filename)
        
        try:
            # Upload the image to S3
            s3_client.upload_fileobj(
                image_data,
                settings.AWS_STORAGE_BUCKET_NAME,
                unique_filename,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
        except Exception as e:
            raise GraphQLError(f"Failed to upload image to S3: {str(e)}")

        # Save the UserImage model instance with the unique filename
        user_image = UserImage(user=user, image_url=unique_filename)
        user_image.save()

        # Construct the full S3 URL
        image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"

        return UploadImage(success=True, image_url=image_url)

# Combine all mutations
class Mutation(graphene.ObjectType):
    register = Register.Field()
    upload_image = UploadImage.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

# Define the schema with both Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
