import graphene
from graphene_django.types import DjangoObjectType
from .models import Task
from django.db import models
from django.contrib.auth.models import User
from graphql_jwt.shortcuts import get_token
from graphql import GraphQLError

# Define a Task type for GraphQL
class TaskType(DjangoObjectType):
    class Meta:
        model = Task

# Define a User type for GraphQL
class UserType(DjangoObjectType):
    class Meta:
        model = User

# Register the Image model
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField()  # Store the S3 URL of the image
    upload_date = models.DateTimeField(auto_now_add=True)

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

# Mutation for obtaining JWT tokens
class ObtainJSONWebToken(graphene.Mutation):
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return ObtainJSONWebToken(token=get_token(user))
        raise GraphQLError('Invalid credentials')

# Combine all mutations
class Mutation(graphene.ObjectType):
    register = Register.Field()
    token_auth = ObtainJSONWebToken.Field()

# Define the schema with both Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
