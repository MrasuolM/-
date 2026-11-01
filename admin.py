from django.contrib import admin
from django import forms
from django.db import models
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.shortcuts import get_object_or_404

from .models import (
    Employee,
    EmployeeMobile,
    EmployeeAddress,
    EmployeeReferrer,
    EmployeeFamilyMember,
    EmployeeDocument,
    EmployeeOrder,
    EmployeeRelative, 
    DeletedEmployeeDocument,
    Department,
    Position,
    Province,
    City,
    
)

from .widgets import PersianDateInput


# =========================================================
# فرم مدیریت پرسنل
# =========================================================

class EmployeeAdminForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # تعداد فرزندان
        # -------------------------------------------------

        self.fields["children_count"].widget = forms.TextInput(
            attrs={
                "class": "vTextField",
                "inputmode": "numeric",
            }
        )

        # -------------------------------------------------
        # گزینه «انتخاب کنید»
        # -------------------------------------------------

        for field in self.fields.values():

            if isinstance(field, forms.ChoiceField):

                choices = list(field.choices)

                if choices and choices[0][0] == "":
                    choices[0] = ("", "انتخاب کنید")

                field.choices = choices

            if isinstance(field, forms.ModelChoiceField):
                field.empty_label = "انتخاب کنید"


# =========================================================
# شماره‌های موبایل
# =========================================================

class EmployeeMobileInline(admin.TabularInline):

    model = EmployeeMobile

    extra = 1

    fields = (
        "number",
        "mobile_type",
        "is_primary",
    )


# =========================================================
# آدرس‌ها
# =========================================================

class EmployeeAddressInline(admin.TabularInline):

    model = EmployeeAddress

    extra = 1

    fields = (
        "province",
        "city",
        "district",
        "full_address",
        "postal_code",
        "landline",
        "from_year",
        "to_year",
        "residence_status",
    )


class EmployeeReferrerInline(admin.StackedInline):
    model = EmployeeReferrer
    extra = 0
    max_num = 1
    can_delete = True
    

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "position",
                    "phone",
                    "address",
                )
            },
        ),
    )


class EmployeeFamilyMemberInline(admin.StackedInline):
    model = EmployeeFamilyMember
    extra = 0
    can_delete = True
    

    
    fieldsets = (
        (
            "اطلاعات عضو خانواده",
            {
                "fields": (
                    "relationship",
                    "first_name",
                    "last_name",
                    "father_name",
                    "national_code",
                    "birth_certificate_number",
                    "birth_date",
                    "birth_place",
                    "marital_status",
                    "mobile",
                    "landline",
                    "occupation",
                    "workplace",
                    "education_level",
                    "field_of_study",
                    "marriage_date",
                    "divorce_date",
                )
            },
        ),
        (
            "پیوست اسناد",
            {
                "fields": (
                    "birth_certificate_file",
                    "national_card_file",
                    "passport_file",
                    "other_document_title",
                    "other_document_file",
                )
            },
        ),
    )

class EmployeeDocumentAdminForm(forms.ModelForm):

    class Meta:
        model = EmployeeDocument
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["file"].widget.attrs.update({
            "accept": ".pdf,.jpg,.jpeg,.png,.gif,.webp,.bmp,.tif,.tiff,.svg"
        })

class EmployeeDocumentInline(admin.TabularInline):

    model = EmployeeDocument
    form = EmployeeDocumentAdminForm

    extra = 0
    can_delete = False

    fields = (
        "document_type",
        "education_level",
        "title",
        "file",
        "issue_date",
        "description",
        "is_deleted",
        "deleted_at",
    )

    
    formfield_overrides = {
        models.DateField: {
            "widget": PersianDateInput(),
        },
    }

    readonly_fields = ("is_deleted", "deleted_at")



    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)


class EmployeeOrderInline(admin.TabularInline):

    model = EmployeeOrder

    extra = 0
    can_delete = True

    fields = (
        "order_type",
        "title",
        "file",
        "issue_date",
        "description",
    )

    formfield_overrides = {
        models.DateField: {
            "widget": PersianDateInput(),
        }
    }

class EmployeeRelativeInline(admin.StackedInline):

    model = EmployeeRelative

    extra = 0
    can_delete = True

    fields = (
        "first_name",
        "last_name",
        "father_name",
        "relationship",
        "position",
        "mobile",
    )

@admin.register(Employee)

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [
        EmployeeMobileInline,
        EmployeeAddressInline,
        EmployeeFamilyMemberInline,
        EmployeeReferrerInline,
        EmployeeDocumentInline,
        EmployeeOrderInline,
        EmployeeRelativeInline,
        
    ]

    form = EmployeeAdminForm
    # -----------------------------------------------------
    # فایل‌های CSS و JavaScript
    # -----------------------------------------------------

    class Media:

        css = {
            "all": (
                "personnel/jalalidatepicker.min.css",
                "personnel/employee-tabs.css",
            )
        }

        js = (
            "personnel/jalalidatepicker.min.js",
            "personnel/companyhr-datepicker.js",
            "personnel/persian-numbers.js",
            "personnel/employee-admin.js",
        )

    # -----------------------------------------------------
    # نمایش تاریخ‌ها با تقویم جلالی
    # -----------------------------------------------------

    formfield_overrides = {
        models.DateField: {
            "widget": PersianDateInput(),
        }
    }

    # -----------------------------------------------------
    # ستون‌های لیست پرسنل
    # -----------------------------------------------------

    list_display = (
        "personnel_code",
        "first_name",
        "last_name",
        "phone",
        "hire_date_jalali",
        "employment_status",
        "department",
        "position",
    )

    # -----------------------------------------------------
    # جست‌وجوی پرسنل
    # -----------------------------------------------------

    search_fields = (
        "personnel_code",
        "first_name",
        "last_name",
        "phone",
        "national_code",
        "father_name",
        "id_number",
        "passport_number",
    )

    # -----------------------------------------------------
    # فیلترهای سمت راست
    # -----------------------------------------------------

    list_filter = (
        "hire_date",
        "employment_status",
        "gender",
        "marital_status",
        "department",
        "position",
        "military_status",
    )

    # -----------------------------------------------------
    # ترتیب نمایش
    # -----------------------------------------------------

    ordering = (
        "personnel_code",
    )

    # -----------------------------------------------------
    # نمایش تاریخ استخدام به صورت جلالی
    # -----------------------------------------------------

    @admin.display(
        description="تاریخ استخدام",
        ordering="hire_date",
    )
    def hire_date_jalali(self, obj):

        if not obj.hire_date:
            return "-"

        import jdatetime

        jalali_date = jdatetime.date.fromgregorian(
            date=obj.hire_date
        )

        date_text = jalali_date.strftime(
            "%Y/%m/%d"
        )

        persian_digits = str.maketrans(
            "0123456789",
            "۰۱۲۳۴۵۶۷۸۹"
        )

        return date_text.translate(
            persian_digits
        )

    # =====================================================
    # تب‌های پرونده پرسنل
                # =====================================================

fieldsets = (

            # =================================================
            # تب ۱ - اطلاعات هویتی
            # =================================================

            (
                "اطلاعات هویتی",
                {
                    "classes": (
                        "tab-fieldset",
                        "tab-hoviat",
                        
                    ),

                    "fields": (

                        # -------------------------------
                        # اطلاعات پایه
                        # -------------------------------

                        "first_name",
                        "last_name",
                        "national_code",
                        "bank_account_status",
                        

                        # -------------------------------
                        # اطلاعات هویتی
                        # -------------------------------

                        "father_name",
                        "previous_last_name",
                        "nickname",

                        "birth_date",
                        "birth_place",

                        "id_number",
                        "id_type",
                        "id_issue_place",
                        "id_issue_date",

                        "duplicate_issue_date",
                        "duplicate_issue_reason",

                        # -------------------------------
                        # جنسیت و تأهل
                        # -------------------------------

                        "gender",
                        "marital_status",
                        "children_count",

                        # -------------------------------
                        # تابعیت و تحصیلات
                        # -------------------------------

                        "religion",
                        "nationality",
                        "has_dual_nationality",
                        "second_nationality",

                        "education_level",
                        "field_of_study",

                        # -------------------------------
                        # گذرنامه
                        # -------------------------------

                        "passport_type",
                        "passport_number",
                        "passport_issue_date",

                        # -------------------------------
                        # خدمت سربازی
                        # -------------------------------

                        "military_status",
                        "military_explanation",
                    ),
                },
            ),

            # =================================================
            # تب ۲ - اطلاعات تماس
            # =================================================

            (
                "اطلاعات تماس",
                {
                    "classes": (
                        "tab-fieldset",
                        "tab-contact",
                    ),

                    "fields": (
                        "landline",
                        "personal_email",
                    ),
                },
            ),

            # =================================================
            # تب ۴ - اطلاعات استخدامی
            # =================================================

            (
                "اطلاعات استخدامی",
                {
                    "classes": (
                        "tab-fieldset",
                        "tab-employment",
                    ),

                    "fields": (
                        # -------------------------------
                        # اطلاعات استخدام
                        # -------------------------------

                        "personnel_code",
                        "hire_date",
                        "employment_status",
                        # -------------------------------
                        # تعلیق
                        # -------------------------------

                            "suspension_start_date",
                            "suspension_end_date",

                        # -------------------------------
                        # پایان همکاری
                        # -------------------------------

                        "termination_date",
                        "termination_reason",
                        "retirement_date",

                        # -------------------------------
                        # اطلاعات سازمانی
                        # -------------------------------

                        "department",
                        "position",

                        # -------------------------------
                        # نوع همکاری و سمت فعلی
                        # -------------------------------

                        "employment_type",
                        "current_position_start_date",

                        # -------------------------------
                        # توضیحات
                        # -------------------------------

                        "employment_notes",
                    ),
                },
            ),
        )

        # =========================================================
        # مدیریت واحد های سازمانی
        # =========================================================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
    )

    search_fields = (

        "name",
    )

    ordering = (
        "name",
    )


# =========================================================
# مدیریت سمت‌ها
# =========================================================

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):

    list_display = (
        
        "title",
        "department",
        "description",
    )

    search_fields = (
       
        "title",
    )

    list_filter = (
        "department",
    )

    ordering = (
        "title",
    )


# =========================================================
# مدیریت شماره موبایل
# =========================================================

@admin.register(EmployeeMobile)
class EmployeeMobileAdmin(admin.ModelAdmin):

    list_display = (
        "number",
        "mobile_type",
        "is_primary",
        "employee",
    )

    search_fields = (
        "number",
        "employee__first_name",
        "employee__last_name",
        "employee__personnel_code",
    )

    list_filter = (
        "mobile_type",
        "is_primary",
    )

    ordering = (
        "employee",
        "-is_primary",
    )


# =========================================================
# مدیریت استان
# =========================================================

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


# =========================================================
# مدیریت شهر
# =========================================================

@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "province",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "province",
    )
# =========================================================
# اسناد پیوست پرسنل
# =========================================================

@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):


    list_display = (
        "employee",
        "document_type",
        "education_level",
        "title",
        "uploaded_at",
    )

    list_filter = (
        "document_type",
        "education_level",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "employee__personnel_code",
        "title",
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)


    formfield_overrides = {
        models.DateField: {
            "widget": PersianDateInput(),
        }
    }

    
    actions = ("restore_documents",)

    @admin.action(description="بازیابی مدارک انتخاب‌شده")
    def restore_documents(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(
                request,
                "فقط مدیر سیستم اجازه بازیابی مدارک را دارد.",
            )
            return

        restored_count = queryset.filter(
            is_deleted=True
        ).update(
            is_deleted=False,
            deleted_at=None,
            deleted_by=None,
        )

        self.message_user(
            request,
            f"تعداد {restored_count} مدرک با موفقیت بازیابی شد.",
        )



@admin.register(DeletedEmployeeDocument)
class DeletedEmployeeDocumentAdmin(admin.ModelAdmin):
    
    list_display = (
        "employee",
        "document_type",
        "education_level",
        "title",
        "deleted_at",
        "deleted_by",
        "permanent_delete_link",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "employee__personnel_code",
        "title",
    )

    list_filter = (
        "document_type",
        "education_level",
    )

    readonly_fields = (
        "employee",
        "document_type",
        "education_level",
        "title",
        "file",
        "issue_date",
        "description",
        "uploaded_at",
        "deleted_at",
        "deleted_by",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            return qs.none()

        return qs.filter(is_deleted=True)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return False
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/permanent-delete/",
                self.admin_site.admin_view(
                    self.permanent_delete_view
                ),
                name="personnel_deletedemployeedocument_permanent_delete",
            ),
        ]
        return custom_urls + urls

   
    @admin.display(description="حذف دائمی")
    def permanent_delete_link(self, obj):
        url = reverse(
            f"{self.admin_site.name}:{self.opts.app_label}_{self.opts.model_name}_permanent_delete",
            args=[obj.pk],
        )
        
        return format_html(
            '<a class="button" href="{}">حذف دائمی</a>',
            url,
        )

    def permanent_delete_view(self, request, object_id):
        if not request.user.is_superuser:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied

        document = get_object_or_404(
            self.get_queryset(request),
            pk=object_id,
        )

        if request.method == "POST":
            file_name = document.file.name if document.file else ""

            shared_file = False
            if file_name:
                shared_file = EmployeeDocument.objects.filter(
                    file=file_name
                ).exclude(pk=document.pk).exists()

            if file_name and not shared_file:
                document.file.storage.delete(file_name)

            document.delete()

            self.message_user(
                request,
                "مدرک از بایگانی حذف دائمی شد.",
            )

            return HttpResponseRedirect(
                reverse(
                    f"admin:{self.opts.app_label}_{self.opts.model_name}_changelist"
                )
            )

        context = {
            **self.admin_site.each_context(request),
            "title": "تأیید حذف دائمی مدرک",
            "opts": self.model._meta,
            "document": document,
            "cancel_url": reverse(
                f"admin:{self.opts.app_label}_{self.opts.model_name}_changelist"
            ),
        }

        return TemplateResponse(
            request,
            "admin/personnel/confirm_permanent_delete.html",
            context,
        )

