from todo.models import TodoModel
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination


class TodoModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'level': ['exact', 'in'],
        'dead_end': ['gte', 'lte']
    }
    search_fields = ['job']
    ordering_fields = ['dead_end', 'updated']
    pagination_class = DefaultPagination

    # get objects
    def get_queryset(self):
        queryset = TodoModel.objects.all()
        if self.request.parser_context.get('kwargs').get('pk'):
            # restrict from reading and editing of others instant task information by permission_classes
            return queryset
        else:
            # restrict from reading of others tasks information
            return queryset.filter(profile__user=self.request.user)
