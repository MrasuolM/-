
from datetime import date, datetime
import jdatetime
from decimal import Decimal, InvalidOperation
from itertools import product

from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.db.models import Q
from django.shortcuts import render

from .models import (
    Department,
    Employee,
    EmployeeMobile,
    EmployeeAddress,
    EmployeeFamilyMember,
    EmployeeDocument,
    EmployeeOrder,
    EmployeeRelative,
    EmployeeReferrer,
)

from contracts.models import (
    Contract,
    ContractParty,
    ContractGuarantee,
    ContractBeneficiary,
    ContractSignatory,
    ContractAddendum,
    ContractHistory,
)


# ---------------------------------------------------------
# تنظیمات فیلترهای پیشرفته
# ---------------------------------------------------------

EMPLOYEE_ADVANCED_FILTERS = {
    "personnel_code": ("کد پرسنلی", "text"),
    "first_name": ("نام", "text"),
    "last_name": ("نام خانوادگی", "text"),
    "father_name": ("نام پدر", "text"),
    "previous_last_name": ("نام خانوادگی قبلی", "text"),
    "nickname": ("نام مستعار", "text"),
    "national_code": ("کد ملی", "text"),
    "id_number": ("شماره شناسنامه", "text"),
    "birth_place": ("محل تولد", "text"),
    "birth_date": ("تاریخ تولد", "date"),
    "gender": ("جنسیت", "choice"),
    "marital_status": ("وضعیت تأهل", "choice"),
    "religion": ("دین", "text"),
    
    "has_dual_nationality": ("تابعیت مضاعف", "boolean"),
    "employment_type": ("نوع استخدام", "choice"),
    "hire_date": ("تاریخ شروع کار", "date"),
    "termination_date": ("تاریخ خاتمه همکاری", "date"),
    "termination_reason": ("علت خاتمه همکاری", "text"),
    "retirement_date": ("تاریخ بازنشستگی", "date"),
    "employment_notes": ("توضیحات استخدام", "text"),
    "education_level": ("مدرک تحصیلی", "text"),
    "field_of_study": ("رشته تحصیلی", "text"),
    "military_status": ("وضعیت نظام‌وظیفه", "choice"),
    "military_explanation": ("توضیحات نظام‌وظیفه", "text"),
    
    "bank_account_status": ("وضعیت حساب بانکی", "choice"),
}

EMPLOYEE_ADVANCED_FILTER_GROUPS = [
    {
        "key": "identity",
        "label": "مشخصات هویتی",
        "fields": [
            "personnel_code", "first_name", "last_name", "father_name",
            "previous_last_name", "nickname", "national_code", "id_number",
            "birth_place", "birth_date", "gender", "marital_status",
            "religion",  "has_dual_nationality",
        ],
    },
    {
        "key": "employment",
        "label": "اطلاعات استخدامی",
        "fields": [
            "employment_type", "hire_date", 
            "termination_date", "termination_reason",
            "retirement_date", "employment_notes",
        ],
    },
    {
        "key": "education",
        "label": "تحصیلات و نظام‌وظیفه",
        "fields": [
            "education_level", "field_of_study", "military_status",
            "military_explanation",
        ],
    },
    
    {
        "key": "bank",
        "label": "اطلاعات بانکی",
        "fields": ["bank_account_status"],
    },
]

RELATED_ADVANCED_FILTERS = {
    "address": {
        "label": "نشانی‌های پرسنل",
        "model": EmployeeAddress,
        "fields": {
            "full_address": ("نشانی", "text"),
            
            "province__name": ("استان", "text"),
            "city__name": ("شهر", "text"),
            
        },
    },
    "family": {
        "label": "اعضای خانواده",
        "model": EmployeeFamilyMember,
        "fields": {
             "first_name": ("نام", "text"),
             "last_name": ("نام خانوادگی", "text"),
             "occupation": ("شغل", "text"),
             "education_level": ("تحصیلات", "text"),
             "field_of_study": ("رشته تحصیلی", "text"),
            },
    },
    "referrer": {
        "label": "معرف پرسنل",
        "model": EmployeeReferrer,
        "fields": {
            "first_name": ("نام", "text"),
            "last_name": ("نام خانوادگی", "text"),
            "position": ("سمت", "text"),
            "phone": ("تلفن", "text"),
            "address": ("نشانی", "text"),
        },
    },
    "relative": {
        "label": "بستگان پرسنل",
        "model": EmployeeRelative,
        "fields": {
            "first_name": ("نام", "text"),
            "last_name": ("نام خانوادگی", "text"),
            "father_name": ("نام پدر", "text"),
            "relationship": ("نسبت", "choice"),
            "position": ("سمت", "text"),
            "mobile": ("تلفن همراه", "text"),
        },
    },
    "order": {
        "label": "احکام پرسنلی",
        "model": EmployeeOrder,
        "fields": {
            "order_type": ("نوع حکم", "choice"),
            "title": ("عنوان حکم", "text"),
            "issue_date": ("تاریخ صدور", "date"),
            "description": ("شرح حکم", "text"),
        },
    },
}

DOCUMENT_ADVANCED_FILTERS = {
    "document_type": ("نوع سند", "choice"),
    "title": ("عنوان سند", "text"),
    "education_level": ("مدرک تحصیلی", "choice"),
    "issue_date": ("تاریخ صدور", "date"),
    "description": ("توضیحات سند", "text"),
}

CONTRACT_ADVANCED_FILTERS = {
    "main": {
        "label": "اطلاعات اصلی قرارداد",
        "fields": {
            "number": ("شماره قرارداد", "text"),
            "contract_type": ("نوع قرارداد", "choice"),
            "subject": ("موضوع قرارداد", "text"),
            "company__name": ("نام شرکت", "text"),
            "second_party__name": ("طرف مقابل قرارداد", "text"),
            "second_party__party_type": ("نوع طرف مقابل", "choice"),
            "status": ("وضعیت قرارداد", "choice"),
            "start_date": ("تاریخ شروع", "date"),
            "end_date": ("تاریخ پایان", "date"),
            "amount": ("مبلغ قرارداد", "number"),
            "currency": ("واحد مبلغ", "text"),
            "duration_description": ("مدت قرارداد", "text"),
            "actual_termination_date": ("تاریخ واقعی خاتمه", "date"),
            "termination_reason": ("علت خاتمه یا فسخ", "text"),
            "attachment_notes": ("توضیحات پیوست‌ها", "text"),
            "notes": ("یادداشت‌ها", "text"),
        },
    },
    "party": {
        "label": "مشخصات طرف مقابل",
        "fields": {
            "second_party__national_id": ("کد ملی یا شناسه ملی", "text"),
            "second_party__registration_number": ("شماره ثبت", "text"),
            "second_party__economic_number": ("شماره اقتصادی", "text"),
            "second_party__representative_name": ("نام نماینده", "text"),
            "second_party__representative_position": ("سمت نماینده", "text"),
            "second_party__phone": ("تلفن طرف مقابل", "text"),
            "second_party__address": ("نشانی طرف مقابل", "text"),
            "second_party__postal_code": ("کد پستی طرف مقابل", "text"),
        },
    },
    "guarantee": {
        "label": "ضمانت‌های قرارداد",
        "fields": {
            "guarantees__guarantee_type": ("نوع ضمانت", "choice"),
            "guarantees__number": ("شماره ضمانت", "text"),
            "guarantees__amount": ("مبلغ ضمانت", "number"),
            "guarantees__issue_date": ("تاریخ صدور ضمانت", "date"),
            "guarantees__maturity_date": ("تاریخ سررسید ضمانت", "date"),
            "guarantees__notes": ("توضیحات ضمانت", "text"),
        },
    },
    "addendum": {
        "label": "الحاقیه‌های قرارداد",
        "fields": {
            "addenda__number": ("شماره الحاقیه", "text"),
            "addenda__addendum_type": ("نوع الحاقیه", "choice"),
            "addenda__date": ("تاریخ الحاقیه", "date"),
            "addenda__revised_start_date": ("تاریخ شروع اصلاح‌شده", "date"),
            "addenda__revised_end_date": ("تاریخ پایان اصلاح‌شده", "date"),
            "addenda__revised_amount": ("مبلغ اصلاح‌شده", "number"),
            "addenda__subject": ("شرح تغییرات", "text"),
            "addenda__notes": ("توضیحات الحاقیه", "text"),
        },
    },
    "beneficiary": {
        "label": "ذی‌نفعان قرارداد",
        "fields": {
            "beneficiaries__name": ("نام ذی‌نفع", "text"),
            "beneficiaries__identifier": ("شناسه ذی‌نفع", "text"),
            "beneficiaries__phone": ("تلفن ذی‌نفع", "text"),
            "beneficiaries__address": ("نشانی ذی‌نفع", "text"),
            "beneficiaries__notes": ("توضیحات ذی‌نفع", "text"),
        },
    },
    "signatory": {
        "label": "امضاکنندگان قرارداد",
        "fields": {
            "signatories__name": ("نام امضاکننده", "text"),
            "signatories__position": ("سمت امضاکننده", "text"),
            "signatories__side": ("طرف قرارداد", "choice"),
            "signatories__national_id": ("کد ملی امضاکننده", "text"),
            "signatories__signature_date": ("تاریخ امضا", "date"),
        },
    },
    "history": {
        "label": "سوابق قرارداد",
        "fields": {
            "history_records__description": ("شرح رویداد", "text"),
            "history_records__created_by__username": ("نام کاربری ثبت‌کننده", "text"),
        },
    },
}


# ---------------------------------------------------------
# توابع عمومی
# ---------------------------------------------------------

def _normalize_search_text(value):
    return str(value or "").replace("ي", "ی").replace("ك", "ک").strip()


def _term_variants(term):
    """ایجاد گونه‌های متداول حروف ی و ک فارسی و عربی."""
    term = str(term or "").strip()
    if not term:
        return []

    variants = {term}
    for char in ("ی", "ي", "ک", "ك"):
        new_variants = set()
        for value in variants:
            if char in value:
                new_variants.add(value.replace(char, "ی" if char in ("ی", "ي") else "ک"))
            if char == "ی" and "ی" in value:
                new_variants.add(value.replace("ی", "ي"))
            if char == "ک" and "ک" in value:
                new_variants.add(value.replace("ک", "ك"))
        variants.update(new_variants)
        if len(variants) > 32:
            break
    return list(variants)[:32]


def _text_query(fields, term):
    query = Q()
    variants = _term_variants(term)
    for field in fields:
        for variant in variants:
            query |= Q(**{f"{field}__icontains": variant})
    return query


def _split_terms(query):
    return [part for part in _normalize_search_text(query).split() if part]

def _date_value(value):
    """تبدیل تاریخ ورودی شمسی یا میلادی به تاریخ قابل فیلتر."""
    value = _normalize_digits(value or "").strip()
    if not value:
        return None

    value = value.replace("-", "/")
    parts = value.split("/")

    if len(parts) != 3:
        return None

    try:
        year, month, day = map(int, parts)

        # ورودی شمسی
        if year < 1700:
            return jdatetime.date(
                year, month, day
            ).togregorian()

        # ورودی میلادی
        return date(year, month, day)

    except (TypeError, ValueError):
        return None
def _field_info(model, path):
    """بررسی ایمن مسیر فیلد، از جمله مسیرهای رابطه‌ای."""
    current_model = model
    parts = path.split("__")
    field = None

    try:
        for part in parts:
            field = current_model._meta.get_field(part)
            if field.is_relation and field.related_model:
                current_model = field.related_model
        return field
    except Exception:
        return None


def _choice_options(model, field_name):
    field = _field_info(model, field_name)
    if field is not None and getattr(field, "choices", None):
        return list(field.choices)
    return []


def _build_filter_fields(model, field_config):
    result = []
    for key, (label, kind) in field_config.items():
        field = _field_info(model, key)
        if field is None:
            continue
        choices = _choice_options(model, key) if kind == "choice" else []
        result.append({
            "key": key,
            "label": label,
            "type": kind,
            "choices": choices,
        })
    return result


def _field_value(request, prefix, key):
    return request.GET.get(f"{prefix}{key}", "").strip()


def _filter_is_active(request, prefix, key, kind):
    if kind == "date":
        range_mode = request.GET.get(f"range_{prefix}{key}") == "1"

        if range_mode:
            return bool(
                _field_value(request, prefix, f"from_{key}")
                or _field_value(request, prefix, f"to_{key}")
            )

        return bool(_field_value(request, prefix, key))

    if kind == "number":
        return any(
            _field_value(request, prefix, f"{part}{key}")
            for part in ("", "min_", "max_")
        )

    return bool(_field_value(request, prefix, key))


def _apply_value_filter(queryset, model, key, kind, request, prefix="f_"):
    """اعمال یک فیلتر؛ فیلدهای خالی هیچ اثری ندارند."""
    field = _field_info(model, key)
    if field is None:
        return queryset, False

   
    if kind == "date":
        range_mode = request.GET.get(f"range_{prefix}{key}") == "1"

        if range_mode:
            start = _date_value(
                _field_value(request, prefix, f"from_{key}")
            )
            end = _date_value(
                _field_value(request, prefix, f"to_{key}")
            )

            if start:
                queryset = queryset.filter(**{f"{key}__gte": start})

            if end:
                queryset = queryset.filter(**{f"{key}__lte": end})

            return queryset, bool(start or end)

        exact = _date_value(_field_value(request, prefix, key))

        if exact:
            queryset = queryset.filter(**{key: exact})

        return queryset, bool(exact)

    if kind == "number":
        raw = _field_value(request, prefix, key)
        min_raw = _field_value(request, prefix, f"min_{key}")
        max_raw = _field_value(request, prefix, f"max_{key}")
        try:
            if raw:
                queryset = queryset.filter(**{key: Decimal(raw.replace(",", ""))})
            if min_raw:
                queryset = queryset.filter(**{f"{key}__gte": Decimal(min_raw.replace(",", ""))})
            if max_raw:
                queryset = queryset.filter(**{f"{key}__lte": Decimal(max_raw.replace(",", ""))})
        except (InvalidOperation, ValueError):
            pass
        return queryset, bool(raw or min_raw or max_raw)

    value = _field_value(request, prefix, key)
    if not value:
        return queryset, False

    operator = request.GET.get(f"op_{key}", "contains")

    if operator == "empty":
        queryset = queryset.filter(Q(**{f"{key}__isnull": True}) | Q(**{key: ""}))
    elif operator == "not_empty":
        queryset = queryset.exclude(Q(**{f"{key}__isnull": True}) | Q(**{key: ""}))
    elif kind == "choice" or operator == "exact":
        queryset = queryset.filter(**{key: value})
    elif kind == "boolean":
        if value in ("yes", "true", "1"):
            queryset = queryset.filter(**{key: True})
        elif value in ("no", "false", "0"):
            queryset = queryset.filter(**{key: False})
    else:
        query = _text_query([key], value)
        queryset = queryset.filter(query)

    return queryset, True


def _apply_configured_filters(queryset, model, config, request, prefix="f_"):
    active = []
    for key, (label, kind) in config.items():
        if not _filter_is_active(request, prefix, key, kind):
            continue
        queryset, applied = _apply_value_filter(
            queryset, model, key, kind, request, prefix
        )
        if applied:
            active.append(label)
    return queryset.distinct(), active


# ---------------------------------------------------------
# جستجوی عمومی در اطلاعات پرسنل
# ---------------------------------------------------------


def _normalize_digits(value):
    """تبدیل ارقام فارسی و عربی به ارقام انگلیسی برای جستجوی یکسان."""
    translation = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789",
    )
    return str(value or "").translate(translation)


def _search_field_label(field):
    labels = {
        # اطلاعات عمومی و شناسایی پرسنل
        "first_name": "نام",
        "last_name": "نام خانوادگی",
        "personnel_code": "کد پرسنلی",
        "national_code": "کد ملی",
        "father_name": "نام پدر",
        "previous_last_name": "نام خانوادگی قبلی",
        "nickname": "نام مستعار",
        "birth_place": "محل تولد",
        "id_number": "شماره شناسنامه",
        "id_issue_place": "محل صدور شناسنامه",
        "passport_number": "شماره گذرنامه",
        "personal_email": "ایمیل شخصی",

        # اطلاعات شغلی و استخدامی
        "department": "واحد سازمانی",
        "department__name": "واحد سازمانی",
        "position": "سمت",
        "position__title": "سمت",
        "employment_status": "وضعیت استخدام",
        "employment_notes": "توضیحات استخدامی",
        "termination_reason": "علت خاتمه همکاری",
        "field_of_study": "رشته تحصیلی",

        # اطلاعات تماس
        "phone": "تلفن همراه",
        "number": "شماره همراه",
        "mobile": "شماره همراه",
        "landline": "تلفن ثابت",
        "personal_email": "ایمیل شخصی",
        "full_address": "نشانی کامل",
        "postal_code": "کد پستی",
        "district": "منطقه",
        "province__name": "استان",
        "city__name": "شهر",

        # اعضای خانواده
        "workplace": "محل کار",
        "occupation": "شغل",
        "education_level": "سطح تحصیلات",
        "relationship": "نسبت خانوادگی",

        # اسناد پرسنلی
        "title": "عنوان",
        "description": "توضیحات",
        "document_type": "نوع سند",

        # احکام پرسنلی
        "order_type": "نوع حکم",

        # بستگان و معرف
        "relationship": "نسبت",
        "address": "نشانی",
    }

    return labels.get(field, field.replace("__", " ← "))


def _employee_results(query):
    queryset = Employee.objects.all()

    # اگر جستجوی متنی خالی باشد، همه پرسنل برمی‌گردند.
    if not query:
        return queryset.distinct()

    main_fields = [
        "first_name", "last_name", "personnel_code", "national_code",
        "phone", "landline", "personal_email", "father_name",
        "previous_last_name", "nickname", "birth_place", "id_number",
        "id_issue_place", "passport_number", "field_of_study",
        "employment_notes", "termination_reason", "department__name",
        "position__title",
    ]
    main_fields = [
        field for field in main_fields
        if _field_info(Employee, field)
    ]

    related_searches = [
        (EmployeeMobile, ["number"]),
        (EmployeeAddress, [
            "full_address", "postal_code", "landline", "district",
            "province__name", "city__name",
        ]),
        (EmployeeFamilyMember, [
            "first_name", "last_name", "father_name", "national_code",
            "mobile", "landline", "workplace", "occupation",
            "education_level", "field_of_study",
        ]),
        (EmployeeDocument, ["title", "description", "document_type"]),
        (EmployeeOrder, ["title", "description", "order_type"]),
        (EmployeeRelative, [
            "first_name", "last_name", "father_name", "relationship",
            "position", "mobile",
        ]),
        (EmployeeReferrer, [
            "first_name", "last_name", "position", "phone", "address",
        ]),
    ]

    # دلیل تطبیق برای هر پرسنل، جداگانه ثبت می‌شود.
    match_reasons = {}

    for term in _split_terms(query):
        normalized_term = _normalize_digits(
            _normalize_search_text(term)
        )
        combined = _text_query(main_fields, term)

        # برای جستجوی کدها و شماره‌ها، گونه‌های عددی هم بررسی می‌شوند.
        numeric_term = _normalize_digits(term)
        if numeric_term != term:
            combined |= _text_query(main_fields, numeric_term)

        # مشخص‌کردن فیلدهای اصلی که با عبارت جستجو تطبیق دارند.
        for employee in Employee.objects.filter(combined).distinct():
            reasons = match_reasons.setdefault(employee.pk, set())

            for field in main_fields:
                value = employee
                try:
                    for part in field.split("__"):
                        value = getattr(value, part)
                    if value is not None:
                        field_text = _normalize_digits(
                            _normalize_search_text(value)
                        )
                        if (
                            normalized_term in field_text
                            or numeric_term in field_text
                        ):  
                            reasons.add(_search_field_label(field))
                except (AttributeError, TypeError):
                    continue

        # جستجو در اطلاعات وابسته به پرونده پرسنلی.
        for related_model, fields in related_searches:
            fields = [
                field for field in fields
                if _field_info(related_model, field)
            ]
            if not fields:
                continue

            related_query = _text_query(fields, term)
            if numeric_term != term:
                related_query |= _text_query(fields, numeric_term)

            related_qs = related_model.objects.filter(related_query)

            employee_fk = next(
                (
                    field.name
                    for field in related_model._meta.fields
                    if isinstance(field, models.ForeignKey)
                    and field.remote_field.model == Employee
                ),
                None,
            )

            if not employee_fk:
                continue

            matched_ids = list(
                related_qs.values_list(
                    f"{employee_fk}_id", flat=True
                ).distinct()
            )

            for related_field in fields:
                field_query = _text_query([related_field], term)

                if numeric_term != term:
                    field_query |= _text_query(
                        [related_field], numeric_term
                    )

                field_employee_ids = related_model.objects.filter(
                    field_query
                ).values_list(
                    f"{employee_fk}_id", flat=True
                ).distinct()

                related_labels = {
                        EmployeeMobile: "شماره همراه",
                        EmployeeAddress: "نشانی",
                        EmployeeFamilyMember: "عضو خانواده",
                        EmployeeDocument: "سند پرسنلی",
                        EmployeeOrder: "حکم پرسنلی",
                        EmployeeRelative: "بستگان",
                        EmployeeReferrer: "معرف",
                    }

                field_label = (
                    f"{related_labels.get(related_model, 'اطلاعات وابسته')} - "
                    f"{_search_field_label(related_field)}"
                )

                for employee_id in field_employee_ids:
                    match_reasons.setdefault(
                        employee_id, set()
                    ).add(field_label)

            combined |= Q(pk__in=matched_ids)

        queryset = queryset.filter(combined)

    # افزودن دلایل تطبیق به هر نتیجه، برای استفاده در قالب جدول.
    results = queryset.distinct()

    for employee in results:
        employee.search_match_reasons = sorted(
            match_reasons.get(employee.pk, set())
        )

    return results

# ---------------------------------------------------------
# جستجوی عمومی در اسناد پیوست
# ---------------------------------------------------------

def _document_results(query):
    queryset = EmployeeDocument.objects.filter(is_deleted=False)

    if not query:
        return queryset

    fields = [
        field for field in
        ["title", "description", "document_type",
         "employee__first_name", "employee__last_name",
         "employee__personnel_code", "employee__national_code"]
        if _field_info(EmployeeDocument, field)
    ]

    for term in _split_terms(query):
        queryset = queryset.filter(_text_query(fields, term))

    return queryset.distinct()


# ---------------------------------------------------------
# جستجوی عمومی در قراردادها و اطلاعات وابسته
# ---------------------------------------------------------

def _contract_results(query):
    queryset = Contract.objects.select_related(
        "company", "second_party"
    ).all()

    if not query:
        return queryset.distinct()

    main_fields = [
        "number", "subject", "duration_description", "notes",
        "attachment_notes", "termination_reason", "company__name",
        "second_party__name", "second_party__national_id",
        "second_party__registration_number", "second_party__economic_number",
        "second_party__phone",
    ]
    main_fields = [field for field in main_fields if _field_info(Contract, field)]

    related_searches = [
        (ContractGuarantee, ["number", "notes"]),
        (ContractBeneficiary, ["name", "identifier", "phone", "address", "party__name"]),
        (ContractSignatory, ["name", "position", "national_id"]),
        (ContractAddendum, ["number", "subject", "notes"]),
        (ContractHistory, ["description"]),
    ]

    for term in _split_terms(query):
        combined = _text_query(main_fields, term)

        for related_model, fields in related_searches:
            fields = [field for field in fields if _field_info(related_model, field)]
            if not fields:
                continue
            related_qs = related_model.objects.filter(_text_query(fields, term))
            contract_fk = next(
                (
                    field.name for field in related_model._meta.fields
                    if isinstance(field, models.ForeignKey)
                    and field.remote_field.model == Contract
                ),
                None,
            )
            if contract_fk:
                combined |= Q(
                    pk__in=related_qs.values_list(f"{contract_fk}_id", flat=True)
                )

        queryset = queryset.filter(combined)

    return queryset.distinct()


# ---------------------------------------------------------
# فیلترهای وابسته به اطلاعات پرسنل
# ---------------------------------------------------------

def _apply_related_group(employees, group_key, group_config, request):
    model = group_config["model"]
    related_qs = model.objects.all()
    active_labels = []

    for key, (label, kind) in group_config["fields"].items():
        prefix = f"f_{group_key}_"
        if not _filter_is_active(request, prefix, key, kind):
            continue
        related_qs, applied = _apply_value_filter(
            related_qs, model, key, kind, request, prefix
        )
        if applied:
            active_labels.append(label)

    if not active_labels:
        return employees, []

    employee_fk = next(
        (
            field.name for field in model._meta.fields
            if isinstance(field, models.ForeignKey)
            and field.remote_field.model == Employee
        ),
        None,
    )
    if not employee_fk:
        return employees, []

    employees = employees.filter(
        pk__in=related_qs.values_list(f"{employee_fk}_id", flat=True)
    ).distinct()

    return employees, active_labels


def _apply_employee_advanced_filters(employees, request):
    active = []

    for key, (label, kind) in EMPLOYEE_ADVANCED_FILTERS.items():
        if not _filter_is_active(request, "f_", key, kind):
            continue
        employees, applied = _apply_value_filter(
            employees, Employee, key, kind, request, "f_"
        )
        if applied:
            active.append(label)

    department_id = request.GET.get("department", "").strip()
    if department_id:
        employees = employees.filter(department_id=department_id)
        active.append("واحد سازمانی")

    employment_status = request.GET.get("employment_status", "").strip()
    if employment_status and _field_info(Employee, "employment_status"):
        employees = employees.filter(employment_status=employment_status)
        active.append("وضعیت استخدام")

    return employees.distinct(), active


def _apply_document_filters(documents, request):
    active = []
    documents, labels = _apply_configured_filters(
        documents, EmployeeDocument, DOCUMENT_ADVANCED_FILTERS, request, "f_doc_"
    )
    active.extend(labels)

    has_photo = request.GET.get("has_photo", "").strip()
    if has_photo:
        photo_field = _field_info(Employee, "photo")
        if photo_field is None:
            photo_field = _field_info(Employee, "image")
        if photo_field is not None:
            if has_photo == "yes":
                documents = documents.exclude(
                    Q(employee__photo__isnull=True) | Q(employee__photo="")
                )
            elif has_photo == "no":
                documents = documents.filter(
                    Q(employee__photo__isnull=True) | Q(employee__photo="")
                )
            active.append("عکس پرسنل")

    return documents.distinct(), active


def _apply_contract_filters(contracts, request):
    active = []
    for group in CONTRACT_ADVANCED_FILTERS.values():
        contracts, labels = _apply_configured_filters(
            contracts, Contract, group["fields"], request, "f_contract_"
        )
        active.extend(labels)

    contract_status = request.GET.get("contract_status", "").strip()
    if contract_status:
        contracts = contracts.filter(status=contract_status)
        active.append("وضعیت قرارداد")

    return contracts.distinct(), active


# ---------------------------------------------------------
# آماده‌سازی گروه‌های نمایشی فیلترها
# ---------------------------------------------------------

def _prepare_employee_groups():
    groups = []
    for group in EMPLOYEE_ADVANCED_FILTER_GROUPS:
        fields = {}
        for key in group["fields"]:
            if key not in EMPLOYEE_ADVANCED_FILTERS:
                continue
            fields[key] = EMPLOYEE_ADVANCED_FILTERS[key]
        groups.append({
            "key": group["key"],
            "label": group["label"],
            "fields": _build_filter_fields(Employee, fields),
        })
    return groups


def _prepare_related_groups():
    groups = []
    for key, config in RELATED_ADVANCED_FILTERS.items():
        groups.append({
            "key": key,
            "label": config["label"],
            "fields": _build_filter_fields(config["model"], config["fields"]),
        })
    return groups


def _prepare_contract_groups():
    groups = []
    for key, config in CONTRACT_ADVANCED_FILTERS.items():
        groups.append({
            "key": key,
            "label": config["label"],
            "fields": _build_filter_fields(Contract, config["fields"]),
        })
    return groups


def _choices_for(model, field_name):
    field = _field_info(model, field_name)
    if field is not None and getattr(field, "choices", None):
        return list(field.choices)
    return []


def _display_filter_value(request, model, key, label, kind, prefix="f_"):
    """ساخت عنوان و مقدار نمایشی فیلتر فعال، بدون تغییر در اعمال فیلتر."""

    if not _filter_is_active(request, prefix, key, kind):
        return None

    if kind == "date":
        range_mode = request.GET.get(f"range_{prefix}{key}") == "1"

        if range_mode:
            start = _field_value(request, prefix, f"from_{key}")
            end = _field_value(request, prefix, f"to_{key}")

            if start and end:
                value = f"از {start} تا {end}"
            elif start:
                value = f"از {start}"
            elif end:
                value = f"تا {end}"
            else:
                return None
        else:
            value = _field_value(request, prefix, key)
            if not value:
                return None

        return {"label": label, "value": value}

    if kind == "number":
        raw = _field_value(request, prefix, key)
        minimum = _field_value(request, prefix, f"min_{key}")
        maximum = _field_value(request, prefix, f"max_{key}")

        parts = []
        if raw:
            parts.append(f"مقدار {raw}")
        if minimum:
            parts.append(f"حداقل {minimum}")
        if maximum:
            parts.append(f"حداکثر {maximum}")

        if not parts:
            return None

        return {"label": label, "value": "، ".join(parts)}

    value = _field_value(request, prefix, key)
    if not value:
        return None

    operator = request.GET.get(f"op_{key}", "contains")

    if operator == "empty":
        display_value = "خالی است"
    elif operator == "not_empty":
        display_value = "خالی نیست"
    else:
        display_value = value

        # تبدیل مقدار گزینه‌های انتخابی به عنوان فارسی
        try:
            field = _field_info(model, key)
            if field is not None and getattr(field, "choices", None):
                choices = dict(field.flatchoices)
                display_value = str(choices.get(value, value))
        except (AttributeError, TypeError, ValueError):
            pass

        if kind == "boolean":
            display_value = {
                "yes": "بله",
                "true": "بله",
                "1": "بله",
                "no": "خیر",
                "false": "خیر",
                "0": "خیر",
            }.get(value, value)

    return {"label": label, "value": display_value}


def _build_active_filter_details(request, model, config, prefix="f_"):
    """فهرست عنوان و مقدار فیلترهای فعال یک بخش."""

    details = []

    for key, (label, kind) in config.items():
        item = _display_filter_value(
            request, model, key, label, kind, prefix
        )
        if item:
            details.append(item)

    return details



# ---------------------------------------------------------
# نمای اصلی جستجو
# ---------------------------------------------------------

@staff_member_required
def companyhr_search(request):
    query = request.GET.get("q", "").strip()
    mode = request.GET.get("mode", "simple")
    if mode not in ("simple", "advanced"):
        mode = "simple"

    can_view_employees = (
        request.user.is_superuser
        or request.user.has_perm("personnel.view_employee")
    )
    can_view_documents = (
        request.user.is_superuser
        or request.user.has_perm("personnel.view_employeedocument")
    )
    can_view_contracts = (
        request.user.is_superuser
        or request.user.has_perm("contracts.view_contract")
    )

    departments = Department.objects.all().order_by("name")

    has_advanced_filter = False
    if mode == "advanced":
        all_configs = [
            ("f_", Employee, EMPLOYEE_ADVANCED_FILTERS),
            ("f_doc_", EmployeeDocument, DOCUMENT_ADVANCED_FILTERS),
        ]
        for prefix, model, config in all_configs:
            if any(
                _filter_is_active(request, prefix, key, kind)
                for key, (_, kind) in config.items()
            ):
                has_advanced_filter = True

        for group_key, config in RELATED_ADVANCED_FILTERS.items():
            prefix = f"f_{group_key}_"
            if any(
                _filter_is_active(request, prefix, key, kind)
                for key, (_, kind) in config["fields"].items()
            ):
                has_advanced_filter = True

        for config in CONTRACT_ADVANCED_FILTERS.values():
            if any(
                _filter_is_active(request, "f_contract_", key, kind)
                for key, (_, kind) in config["fields"].items()
            ):
                has_advanced_filter = True

    department_id = request.GET.get("department", "").strip()
    employment_status = request.GET.get("employment_status", "").strip()
    contract_status = request.GET.get("contract_status", "").strip()
    has_photo = request.GET.get("has_photo", "").strip()

    has_filters = bool(
        (mode == "advanced" and has_advanced_filter)
        or department_id
        or employment_status
        or contract_status
        or has_photo
    )
    should_search = bool(query or has_filters)

    employees = Employee.objects.none()
    documents = EmployeeDocument.objects.none()
    contracts = Contract.objects.none()

    active_employee_filters = []
    active_document_filters = []
    active_contract_filters = []

    if should_search and can_view_employees:
        employees = _employee_results(query)

        employee_match_reasons = {
            employee.pk: getattr(employee, "search_match_reasons", [])
            for employee in employees
        }

        if mode == "advanced":
            employees, active_employee_filters = _apply_employee_advanced_filters(
                employees, request
            )

            for group_key, config in RELATED_ADVANCED_FILTERS.items():
                employees, labels = _apply_related_group(
                    employees, group_key, config, request
                )
                active_employee_filters.extend(labels)

        employees = employees.distinct()
        for employee in employees:
            employee.search_match_reasons = employee_match_reasons.get(
                employee.pk, []
            )

    if should_search and can_view_documents:
        documents = _document_results(query)

        if department_id and _field_info(EmployeeDocument, "employee__department"):
            documents = documents.filter(employee__department_id=department_id)

        if employment_status and _field_info(
            EmployeeDocument, "employee__employment_status"
        ):
            documents = documents.filter(
                employee__employment_status=employment_status
            )

        if mode == "advanced":
            documents, active_document_filters = _apply_document_filters(
                documents, request
            )

        documents = documents.distinct()

    if should_search and can_view_contracts:
        contracts = _contract_results(query)

        if mode == "advanced":
            contracts, active_contract_filters = _apply_contract_filters(
                contracts, request
            )
        elif contract_status:
            contracts = contracts.filter(status=contract_status)

        contracts = contracts.distinct()

    # محدودکردن فیلترهای بخش‌ها بر اساس مجوز کاربر
    if not can_view_employees:
        employees = Employee.objects.none()
    if not can_view_documents:
        documents = EmployeeDocument.objects.none()
    if not can_view_contracts:
        contracts = Contract.objects.none()

    employee_count = employees.count()
    document_count = documents.count()
    contract_count = contracts.count()
    total_count = employee_count + document_count + contract_count

    
    # اطلاعات نمایشی فیلترهای پیشرفته هر بخش
    active_employee_filter_details = []
    active_document_filter_details = []
    active_contract_filter_details = []

    if mode == "advanced":
        if can_view_employees:
            active_employee_filter_details = _build_active_filter_details(
                request,
                Employee,
                EMPLOYEE_ADVANCED_FILTERS,
                "f_",
            )

            for group_key, config in RELATED_ADVANCED_FILTERS.items():
                items = _build_active_filter_details(
                    request,
                    config["model"],
                    config["fields"],
                    f"f_{group_key}_",
                )
                active_employee_filter_details.extend(items)

        if can_view_documents:
            active_document_filter_details = _build_active_filter_details(
                request,
                EmployeeDocument,
                DOCUMENT_ADVANCED_FILTERS,
                "f_doc_",
            )

        if can_view_contracts:
            active_contract_filter_details = _build_active_filter_details(
                request,
                Contract,
                CONTRACT_ADVANCED_FILTERS,
                "f_contract_",
            )


    context = {
        "title": "جستجوی اطلاعات",
        "query": query,
        "mode": mode,
        "department_id": department_id,
        "employment_status": employment_status,
        "contract_status": contract_status,
        "has_photo": has_photo,

        "employee_filter_groups": _prepare_employee_groups(),
        "related_filter_groups": _prepare_related_groups(),
        "contract_filter_groups": _prepare_contract_groups(),
        "document_filter_fields": _build_filter_fields(
            EmployeeDocument, DOCUMENT_ADVANCED_FILTERS
        ),

        "employee_filter_fields": EMPLOYEE_ADVANCED_FILTERS,
        "departments": departments,
        "employment_status_choices": _choices_for(Employee, "employment_status"),
        "contract_status_choices": Contract.STATUS_CHOICES,
        "contract_type_choices": Contract.CONTRACT_TYPES,

        "active_employee_filters": active_employee_filters,
        "active_document_filters": active_document_filters,
        "active_contract_filters": active_contract_filters,

                
        "active_employee_filter_details": active_employee_filter_details,
        "active_document_filter_details": active_document_filter_details,
        "active_contract_filter_details": active_contract_filter_details,


        "employees": employees,
        "documents": documents,
        "contracts": contracts,

        "employee_count": employee_count,
        "document_count": document_count,
        "contract_count": contract_count,
        "total_count": total_count,
        "should_search": should_search,

        "can_view_employees": can_view_employees,
        "can_view_documents": can_view_documents,
        "can_view_contracts": can_view_contracts,
    }

    return render(request, "personnel/search.html", context)
