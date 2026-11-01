
from django.urls import path

from .api.cities import cities_by_province
from .views import soft_delete_employee_document
from .access_control.views import (
    user_management,
    group_management,
    permissions_management,
)
from .search_views import companyhr_search
urlpatterns = [
    path(
        "cities-by-province/",
        cities_by_province,
        name="cities_by_province",
    ),
    path(
        "documents/<int:document_id>/soft-delete/",
        soft_delete_employee_document,
        name="soft_delete_employee_document",
    ),

    path(
        "access/users/",
        user_management,
        name="personnel_access_users",
    ),

    path(
        "access/groups/",
        group_management,
        name="personnel_access_groups",
    ),

    path(
         "access/permissions/",
          permissions_management,
          name="personnel_access_permissions",
        ),

    path(
    "search/",
    companyhr_search,
    name="personnel_companyhr_search",
    ),    
]
