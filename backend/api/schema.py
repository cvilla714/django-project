import graphene
from graphene_django.types import DjangoObjectType
from .models import Task

# Define a Task type for GraphQL
class TaskType(DjangoObjectType):
    class Meta:
        model = Task

# Create a Query class that returns all tasks
class Query(graphene.ObjectType):
    tasks = graphene.List(TaskType)

    def resolve_tasks(self, info, **kwargs):
        return Task.objects.all()

# Define the schema
schema = graphene.Schema(query=Query)
