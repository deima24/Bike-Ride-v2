from . import views
from django.urls import path


urlpatterns = [
    path("", views.EntryList.as_view(), name="entry"),
    path('<slug:slug>', views.EntryDetail.as_view(), name='entry_detail'),
    path('edit/<slug:pk>', views.EntryEdit.as_view(), name='entry_edit')
]