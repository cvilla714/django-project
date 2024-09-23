from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from backend.api.schema import schema
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the Django-GraphQL App")

urlpatterns = [
    path('', home_view),  # Root URL
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
