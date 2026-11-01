
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import EmployeeDocument


@staff_member_required
@require_POST
def soft_delete_employee_document(request, document_id):
    """
    حذف نرم پیوست پرسنل؛ رکورد و فایل اصلی حفظ می‌شوند.
    """

    document = get_object_or_404(
        EmployeeDocument,
        pk=document_id,
    )

    if not request.user.has_perm("personnel.change_employeedocument"):
        return JsonResponse(
            {
                "success": False,
                "message": "شما مجوز حذف این پیوست را ندارید.",
            },
            status=403,
        )

    if not document.is_deleted:
        document.is_deleted = True
        document.deleted_at = timezone.now()
        document.deleted_by = request.user

        document.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
                "deleted_by",
            ]
        )

    return JsonResponse(
        {
            "success": True,
            "message": "پیوست به‌صورت نرم حذف شد.",
        }
    )

