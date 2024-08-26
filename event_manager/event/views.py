from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from event import models
from event.filters import EventFilter
from event.pagination import EventPagination
from event.permissions import IsCreatorOrReadOnly
from event.serializers import (
    ErrorResponseSerializer,
    EventSerializer,
    SuccessResponseSerializer,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of all events, with optional filtering by start date, end date, creator and type.",
        summary="List Events",
        parameters=[
            OpenApiParameter(
                name="start_date",
                description="Filter by start date (YYYY-MM-DD)",
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name="end_date",
                description="Filter by end date (YYYY-MM-DD)",
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name="created_by",
                description="Filter by creator username",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="type",
                description="Filter by event type",
                type=OpenApiTypes.STR,
                enum=[choice.value for choice in models.EventTypeEnum],
            ),
        ],
    ),
    retrieve=extend_schema(
        description="Retrieve details of a specific event by its ID.",
        summary="Retrieve Event",
    ),
    create=extend_schema(
        description="Create a new event. Only authenticated users can create events.",
        summary="Create Event",
    ),
    update=extend_schema(
        description="Update an existing event. Only the creator of the event can update it.",
        summary="Update Event",
    ),
    partial_update=extend_schema(
        description="Partially update an existing event. Only the creator of the event can update it.",
        summary="Partial Update Event",
    ),
    destroy=extend_schema(
        description="Delete an existing event. Only the creator of the event can delete it.",
        summary="Delete Event",
    ),
)
class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all().order_by("start_date")
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
    pagination_class = EventPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(
        description="Register the authenticated user for the event. Only future events can be registered.",
        summary="Register for Event",
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
        },
        request=None,
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()

        if event.is_past_event():
            return Response(
                {"detail": "Cannot register for past events."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if event.attendees.count() >= event.capacity:
            return Response(
                {"detail": "Event capacity reached."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event.attendees.add(request.user)

        return Response(
            {"detail": "Successfully registered for the event."},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        description="Unregister the authenticated user from the event. Only future events can be unregistered.",
        summary="Unregister from Event",
        responses={
            200: SuccessResponseSerializer,
            400: ErrorResponseSerializer,
            403: ErrorResponseSerializer,
        },
        request=None,
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def unregister(self, request, pk=None):
        event = self.get_object()

        if event.is_past_event():
            return Response(
                {"detail": "Cannot unregister from past events."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        event.attendees.remove(request.user)

        return Response(
            {"detail": "Successfully unregistered from the event."},
            status=status.HTTP_200_OK,
        )
