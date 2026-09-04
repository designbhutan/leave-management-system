from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("apply/", views.apply_leave, name="apply_leave"),
    path("my-leaves/", views.my_leaves, name="my_leaves"),
    path("supervisor/", views.supervisor_dashboard, name="supervisor_dashboard"),
    path("supervisor/leave/<int:pk>/", views.review_leave, name="review_leave"),
    path("supervisor/leave/<int:pk>/cancel-review/", views.cancel_review, name="cancel_review"),
]
