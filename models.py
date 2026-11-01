from django.db import models
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(
        "نام واحد سازمانی",
        max_length=100,
        unique=True
    )

    

    description = models.TextField(
        "توضیحات",
        blank=True
    )

    class Meta:
      verbose_name = "واحد سازمانی"
      verbose_name_plural = "واحدهای سازمانی"

    def __str__(self):
      return self.name


class Position(models.Model):
    title = models.CharField(
        "عنوان سمت",
        max_length=100,
        unique=True
    )

   

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name="واحد سازمانی",
        null=True,
        blank=True
    )

    description = models.TextField(
        "توضیحات",
        blank=True
    )
    class Meta:
      verbose_name = "سمت"
      verbose_name_plural = "سمت‌ها"

    def __str__(self):
        return self.title
class Province(models.Model):
    name = models.CharField(
        "نام استان",
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان‌ها"

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="cities",
        verbose_name="استان"
    )

    name = models.CharField(
        "نام شهر",
        max_length=100
    )

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"
        unique_together = ("province", "name")

    def __str__(self):
        return self.name


class Employee(models.Model):

    # =========================
    # اطلاعات پایه
    # =========================

    first_name = models.CharField(
        "نام",
        max_length=100
    )

    last_name = models.CharField(
        "نام خانوادگی",
        max_length=100
    )

    personnel_code = models.CharField(
        "کد پرسنلی",
        max_length=50,
        unique=True
    )

    BANK_ACCOUNT_STATUS_CHOICES = [
            ("yes", "دارد"),
            ("no", "ندارد"),
        ]
    
    bank_account_status = models.CharField(
            "وضعیت شماره حساب",
            max_length=3,
            choices=BANK_ACCOUNT_STATUS_CHOICES,
            default="no",
        )
    

    phone = models.CharField(
        "شماره تماس",
        max_length=20,
        blank=True
    )
    landline = models.CharField(
    "تلفن ثابت",
    max_length=20,
    blank=True
    )

    personal_email = models.EmailField(
      "ایمیل شخصی",
       max_length=254,
       blank=True
     )

    national_code = models.CharField(
        "کد ملی",
        max_length=10,
        unique=True
    )

    birth_certificate_serial = models.CharField(
    "سریال شناسنامه",
    max_length=20,
    blank=True,
    )

    hire_date = models.DateField(
        "تاریخ استخدام"
    )
    EMPLOYMENT_STATUS_CHOICES = [
        ("active", "فعال"),
        ("suspended", "تعلیق"),
        ("terminated", "خاتمه همکاری"),
        ("retired", "بازنشسته"),
        ("other", "سایر"),
    ]

    employment_status = models.CharField(
         "وضعیت استخدام",
         max_length=20,
         choices=EMPLOYMENT_STATUS_CHOICES,
         default="active",
        )

    suspension_start_date = models.DateField(
       "تاریخ شروع تعلیق",
        null=True,
        blank=True
)

    suspension_end_date = models.DateField(
      "تاریخ پایان تعلیق",
        null=True,
        blank=True
)

    termination_date = models.DateField(
        "تاریخ خاتمه همکاری",
        null=True,
        blank=True,
    )

    termination_reason = models.TextField(
        "علت خاتمه همکاری",
        blank=True,
    )

    retirement_date = models.DateField(
        "تاریخ بازنشستگی",
        null=True,
        blank=True,
    )
    
    # =====================================================
    # تکمیل اطلاعات استخدامی
    # =====================================================

    EMPLOYMENT_TYPE_CHOICES = [
        ("full_time", "تمام‌وقت"),
        ("part_time", "پاره‌وقت"),
        ("contractual", "قراردادی"),
        ("probationary", "آزمایشی"),
        ("other", "سایر"),
]

    employment_type = models.CharField(
        "نوع همکاری",
         max_length=20,
         choices=EMPLOYMENT_TYPE_CHOICES,
         blank=True,
)

    current_position_start_date = models.DateField(
         "تاریخ شروع سمت فعلی",
          null=True,
          blank=True,
)

    employment_notes = models.TextField(
       "توضیحات استخدامی",
        blank=True,
)
    photo = models.ImageField(
        "عکس پرسنلی",
        upload_to="employees/photos/",
        null=True,
        blank=True,
    )

    # =========================
    # اطلاعات هویتی
    # =========================

    father_name = models.CharField(
        "نام پدر",
        max_length=100,
        blank=True
    )
    
    
    previous_last_name = models.CharField(
        "نام خانوادگی قبلی",
        max_length=100,
        blank=True
    )

    nickname = models.CharField(
        "شهرت / لقب",
        max_length=100,
        blank=True
    )

    birth_date = models.DateField(
        "تاریخ تولد",
        null=True,
        blank=True
    )

    birth_place = models.CharField(
        "محل تولد",
        max_length=100,
        blank=True
    )

    id_number = models.CharField(
        "شماره شناسنامه",
        max_length=20,
        blank=True
    )

    id_issue_place = models.CharField(
        "محل صدور شناسنامه",
        max_length=100,
        blank=True
    )

    id_issue_date = models.DateField(
        "تاریخ صدور شناسنامه",
        null=True,
        blank=True
    )

    ID_TYPE_CHOICES = [
        ("original", "اصل"),
        ("duplicate", "المثنی"),
    ]

    id_type = models.CharField(
        "نوع شناسنامه",
        max_length=20,
        choices=ID_TYPE_CHOICES,
        blank=True
    )

    duplicate_issue_date = models.DateField(
        "تاریخ صدور المثنی",
        null=True,
        blank=True
    )

    duplicate_issue_reason = models.CharField(
        "علت صدور المثنی",
        max_length=200,
        blank=True
    )

    # =========================
    # جنسیت و وضعیت تأهل
    # =========================

    GENDER_CHOICES = [
        ("male", "مرد"),
        ("female", "زن"),
    ]

    gender = models.CharField(
        "جنسیت",
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )

    MARITAL_STATUS_CHOICES = [
        ("single", "مجرد"),
        ("married", "متأهل"),
        ("divorced", "مطلق"),
        ("widowed", "همسر فوت‌شده"),
    ]

    marital_status = models.CharField(
        "وضعیت تأهل",
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True
    )

    children_count = models.PositiveIntegerField(
        "تعداد فرزندان",
        default=0
    )

    # =========================
    # اطلاعات تابعیت و تحصیلات
    # =========================

    religion = models.CharField(
        "مذهب",
        max_length=100,
        blank=True
    )

    nationality = models.CharField(
        "تابعیت",
        max_length=100,
        blank=True
    )

    has_dual_nationality = models.BooleanField(
        "تابعیت مضاعف",
        default=False
    )

    second_nationality = models.CharField(
        "تابعیت دوم",
        max_length=100,
        blank=True
    )

    education_level = models.CharField(
        "آخرین مدرک تحصیلی",
        max_length=100,
        blank=True
    )

    field_of_study = models.CharField(
        "رشته تحصیلی",
        max_length=150,
        blank=True
    )

    # =========================
    # اطلاعات گذرنامه
    # =========================

    PASSPORT_TYPE_CHOICES = [
        ("ordinary", "عادی"),
        ("diplomatic", "سیاسی"),
        ("service", "خدمت"),
        ("special", "خاص"),
    ]

    passport_type = models.CharField(
        "نوع گذرنامه",
        max_length=20,
        choices=PASSPORT_TYPE_CHOICES,
        blank=True
    )

    passport_number = models.CharField(
        "شماره گذرنامه",
        max_length=50,
        blank=True
    )

    passport_issue_date = models.DateField(
        "تاریخ صدور گذرنامه",
        null=True,
        blank=True
    )

    # =========================
    # وضعیت خدمت سربازی
    # =========================

    MILITARY_STATUS_CHOICES = [
        ("not_applicable", "مشمول نیست"),
        ("completed", "پایان خدمت"),
        ("exempt", "معاف"),
        ("in_progress", "در حال خدمت"),
        ("other", "سایر"),
    ]

    military_status = models.CharField(
        "وضعیت خدمت سربازی",
        max_length=30,
        choices=MILITARY_STATUS_CHOICES,
        blank=True
    )
    military_explanation = models.CharField(
      "توضیحات وضعیت خدمت سربازی",
      max_length=200,
      blank=True
     )

    # =========================
    # اطلاعات سازمانی
    # =========================

    department = models.ForeignKey(
      Department,
      on_delete=models.PROTECT,
      verbose_name="واحد سازمانی",
      null=True,
      blank=True
)

    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        verbose_name="سمت",
        null=True,
        blank=True
)
    class Meta:
      verbose_name = "پرسنل"
      verbose_name_plural = "پرسنل"
    def __str__(self):
     return f"{self.first_name} {self.last_name}"


# =========================================================
# معرف پرسنل
# =========================================================


    
class EmployeeReferrer(models.Model):

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="referrer",
        verbose_name="پرسنل",
    )

    first_name = models.CharField(
        "نام معرف",
        max_length=100,
    )

    last_name = models.CharField(
        "نام خانوادگی معرف",
        max_length=100,
    )

    position = models.CharField(
        "سمت معرف",
        max_length=150,
        blank=True,
    )

    phone = models.CharField(
        "شماره تماس معرف",
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        "آدرس معرف",
        blank=True,
    )

    class Meta:
        verbose_name = "معرف پرسنل"
        verbose_name_plural = "معرف‌های پرسنل"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class EmployeeMobile(models.Model):

    MOBILE_TYPE_CHOICES = [
        ("personal", "شخصی"),
        ("work", "کاری"),
        ("other", "سایر"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="mobile_numbers",
        verbose_name="پرسنل",
    )

    number = models.CharField(
        "شماره موبایل",
        max_length=20,
    )

    mobile_type = models.CharField(
        "نوع شماره",
        max_length=20,
        choices=MOBILE_TYPE_CHOICES,
        default="personal",
    )

    is_primary = models.BooleanField(
        "شماره اصلی",
        default=False,
    )

    class Meta:
        verbose_name = "شماره موبایل"
        verbose_name_plural = "شماره‌های موبایل"

    def __str__(self):
        return self.number
    
class EmployeeAddress(models.Model):

    RESIDENCE_STATUS_CHOICES = [
        ("current", "جاری"),
        ("previous", "قبلی"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="پرسنل",
    )

    province = models.ForeignKey(
    Province,
    on_delete=models.PROTECT,
    verbose_name="استان",
    related_name="employee_addresses",
    )

    city = models.ForeignKey(
     City,
     on_delete=models.PROTECT,
     verbose_name="شهر",
     related_name="employee_addresses",
     )

    district = models.CharField(
        "شهرستان / منطقه",
        max_length=100,
        blank=True,
    )

    full_address = models.TextField(
        "آدرس کامل",
    )

    postal_code = models.CharField(
        "کد پستی",
        max_length=20,
        blank=True,
    )

    landline = models.CharField(
        "تلفن ثابت مرتبط با آدرس",
        max_length=20,
        blank=True,
    )

    from_year = models.PositiveIntegerField(
        "از سال",
        null=True,
        blank=True,
    )

    to_year = models.PositiveIntegerField(
        "تا سال",
        null=True,
        blank=True,
    )

    residence_status = models.CharField(
        "وضعیت سکونت",
        max_length=20,
        choices=RESIDENCE_STATUS_CHOICES,
        default="current",
    )

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"

    def __str__(self):
        return f"{self.employee} - {self.city}"


class EmployeeFamilyMember(models.Model):
    RELATIONSHIP_CHOICES = [
        ("current_spouse", "همسر فعلی"),
        ("second_spouse", "همسر دوم"),
        ("former_spouse", "همسر سابق"),
        ("father", "پدر"),
        ("mother", "مادر"),
        ("child", "فرزند"),
        ("brother", "برادر"),
        ("sister", "خواهر"),
        ("other", "سایر"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("single", "مجرد"),
        ("married", "متأهل"),
        ("divorced", "مطلقه"),
        ("widowed", "همسر فوت شده"),
        ("other", "سایر"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="family_members",
        verbose_name="پرسنل",
    )

    relationship = models.CharField(
        "نسبت",
        max_length=30,
        choices=RELATIONSHIP_CHOICES,
    )

    first_name = models.CharField(
        "نام",
        max_length=100,
    )

    last_name = models.CharField(
        "نام خانوادگی",
        max_length=100,
    )

    father_name = models.CharField(
        "نام پدر",
        max_length=100,
        blank=True,
    )

    national_code = models.CharField(
        "کد ملی",
        max_length=10,
        blank=True,
    )

    birth_certificate_number = models.CharField(
        "شماره شناسنامه",
        max_length=50,
        blank=True,
    )

    birth_date = models.DateField(
        "تاریخ تولد",
        null=True,
        blank=True,
    )

    birth_place = models.CharField(
        "محل تولد",
        max_length=100,
        blank=True,
    )

    marital_status = models.CharField(
        "وضعیت تأهل",
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
    )

    mobile = models.CharField(
        "شماره موبایل",
        max_length=20,
        blank=True,
    )

    landline = models.CharField(
        "تلفن ثابت",
        max_length=20,
        blank=True,
    )

    workplace = models.CharField(
        "محل کار",
        max_length=200,
        blank=True,
    )

    occupation = models.CharField(
        "شغل",
        max_length=150,
        blank=True,
    )

    education_level = models.CharField(
        "مدرک تحصیلی",
        max_length=100,
        blank=True,
    )

    field_of_study = models.CharField(
        "رشته تحصیلی",
        max_length=150,
        blank=True,
    )

    marriage_date = models.DateField(
        "تاریخ ازدواج",
        null=True,
        blank=True,
    )

    divorce_date = models.DateField(
        "تاریخ طلاق",
        null=True,
        blank=True,
    )

        # =========================
    # پیوست اسناد
    # =========================

    birth_certificate_file = models.FileField(
        "فایل شناسنامه",
        upload_to="family/birth_certificate/%Y/%m/",
        null=True,
        blank=True,
    )

    national_card_file = models.FileField(
        "فایل کارت ملی",
        upload_to="family/national_card/%Y/%m/",
        null=True,
        blank=True,
    )

    passport_file = models.FileField(
        "فایل گذرنامه",
        upload_to="family/passport/%Y/%m/",
        null=True,
        blank=True,
    )

    other_document_title = models.CharField(
        "عنوان سایر مدارک",
        max_length=200,
        blank=True,
    )

    other_document_file = models.FileField(
        "فایل سایر مدارک",
        upload_to="family/other/%Y/%m/",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "عضو خانواده"
        verbose_name_plural = "اعضای خانواده"

    def __str__(self):
        relationship = self.get_relationship_display() if self.relationship else ""
        name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        if relationship and name:
            return f"{relationship} - {name}"
        return relationship or name or "عضو خانواده"



VIDEO_EXTENSIONS = {
          ".mp4", ".mov", ".avi", ".mkv",
          ".3gp", ".m4v", ".mpeg", ".mpg",
          ".wmv", ".flv", ".webm",
          ".ts", ".mts", ".m2ts",
          ".vob", ".asf",
          ".dav", ".264", ".h264",
          ".265", ".h265",
         }      
    


def validate_employee_document_file(value):
    from pathlib import Path
    from django.core.exceptions import ValidationError
    from django.core.files.uploadedfile import UploadedFile

    max_size = 20 * 1024 * 1024

    # کنترل حجم فقط برای فایلی که همین حالا بارگذاری می‌شود
    if isinstance(value, UploadedFile):
        if value.size > max_size:
            raise ValidationError(
                "حجم فایل نباید بیشتر از ۲۰ مگابایت باشد."
            )

    # بررسی پسوند فایل
    file_name = getattr(value, "name", "")

    if not file_name:
        return

    extension = Path(file_name).suffix.lower()

    if not extension:
        raise ValidationError(
            "فایل باید پسوند معتبر داشته باشد."
        )

    allowed_extensions = {
        ".pdf", ".jpg", ".jpeg", ".png", ".gif",
        ".webp", ".bmp", ".tif", ".tiff", ".svg",
    }

    if (
        extension not in allowed_extensions
        and extension not in VIDEO_EXTENSIONS
    ):
        raise ValidationError(
            "فرمت فایل مجاز نیست."
        )

    from pathlib import Path
    from django.core.exceptions import ValidationError
    from django.core.files.uploadedfile import UploadedFile

    # حداکثر حجم مجاز: ۲۰ مگابایت
    max_size = 20 * 1024 * 1024

    # فایل جدیدی که کاربر انتخاب کرده است
    if isinstance(value, UploadedFile):
        file_size = value.size
    else:
        # فایل قبلی که در مدل ثبت شده است
        try:
            file_size = value.size
        except (OSError, FileNotFoundError):
            raise ValidationError(
                "فایل قبلی در مسیر ذخیره‌سازی پیدا نشد. "
                "لطفاً فایل را دوباره انتخاب و بارگذاری کنید."
            )

    if file_size > max_size:
        raise ValidationError(
            "حجم فایل نباید بیشتر از ۲۰ مگابایت باشد."
        )

    allowed_extensions = {
        ".pdf",
        ".jpg", ".jpeg", ".png", ".gif",
        ".webp", ".bmp", ".tif", ".tiff",
        ".svg",
    }

    # پسوندهای ویدئویی که در سطح ماژول تعریف شده‌اند
    file_name = value.name.lower()
    extension = Path(file_name).suffix

    if not extension:
        raise ValidationError(
            "فایل باید پسوند معتبر داشته باشد."
        )

    if (
        extension not in allowed_extensions
        and extension not in VIDEO_EXTENSIONS
    ):
        raise ValidationError(
            "فرمت فایل مجاز نیست."
        )

class EmployeeDocument(models.Model):

    DOCUMENT_TYPE_CHOICES = [
        ("birth_certificate", "شناسنامه"),
        ("national_card", "کارت ملی"),
        ("education", "مدرک تحصیلی"),
        ("no_criminal_record", "گواهی سوء پیشینه"),
        ("military_card", "کارت پایان خدمت"),
        ("passport", "گذرنامه"),
        ("other", "سایر مستندات"),
    ]

    EDUCATION_LEVEL_CHOICES = [
        ("diploma", "دیپلم"),
        ("associate", "فوق دیپلم"),
        ("bachelor", "کارشناسی"),
        ("master", "کارشناسی ارشد"),
        ("phd", "دکترا"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="documents",
        verbose_name="پرسنل",
    )

    document_type = models.CharField(
        "نوع سند",
        max_length=30,
        choices=DOCUMENT_TYPE_CHOICES,
    )

    education_level = models.CharField(
        "سطح مدرک تحصیلی",
        max_length=20,
        choices=EDUCATION_LEVEL_CHOICES,
        blank=True,
        help_text="فقط برای نوع «مدرک تحصیلی»",
    )

    title = models.CharField(
        "عنوان / توضیح کوتاه",
        max_length=200,
        blank=True,
    )

    file = models.FileField(
         "فایل",
         upload_to="employees/documents/%Y/%m/",
         validators=[validate_employee_document_file],
        )

    issue_date = models.DateField(
        "تاریخ صدور",
        null=True,
        blank=True,
    )

    description = models.TextField(
        "توضیحات",
        blank=True,
    )

    uploaded_at = models.DateTimeField(
        "تاریخ بارگذاری",
        auto_now_add=True,
    )

    is_deleted = models.BooleanField(
        "حذف شده",
        default=False,
    )

    deleted_at = models.DateTimeField(
        "تاریخ حذف",
        null=True,
        blank=True,
    )
    
    deleted_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="حذف‌کننده",
        related_name="deleted_employee_documents",
    )


    def clean(self):
        super().clean()

        if not self.file:
            return

        file_name = self.file.name.lower()

        if "." not in file_name:
            return

        extension = "." + file_name.rsplit(".", 1)[1]

        if (
            extension in VIDEO_EXTENSIONS
            and self.document_type != "other"
        ):
            raise ValidationError({
                "file": (
                    "فایل ویدئویی فقط در نوع مدرک «سایر» "
                    "مجاز است."
                )
            })

    class Meta:
        verbose_name = "سند پیوست"
        verbose_name_plural = "اسناد پیوست"
        ordering = ["document_type", "education_level", "id"]

    def __str__(self):
        if self.document_type == "education" and self.education_level:
            return f"{self.get_document_type_display()} - {self.get_education_level_display()}"
        return self.get_document_type_display()

class EmployeeOrder(models.Model):

    ORDER_TYPE_CHOICES = [
        ("appointment", "حکم کارگزینی"),
        ("reward", "حکم تشویقی"),
        ("disciplinary", "حکم انضباطی"),
        ("other", "سایر"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="پرسنل",
    )

    order_type = models.CharField(
        "نوع حکم",
        max_length=20,
        choices=ORDER_TYPE_CHOICES,
    )

    title = models.CharField(
        "عنوان",
        max_length=200,
        blank=True,
    )

    file = models.FileField(
        "فایل",
        upload_to="employees/orders/%Y/%m/",
        validators=[validate_employee_document_file],
     )

    issue_date = models.DateField(
        "تاریخ صدور",
        null=True,
        blank=True,
    )

    description = models.TextField(
        "توضیحات",
        blank=True,
    )

    uploaded_at = models.DateTimeField(
        "تاریخ بارگذاری",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "حکم"
        verbose_name_plural = "احکام"
        ordering = ["order_type", "id"]

    def __str__(self):
        if self.title:
            return f"{self.get_order_type_display()} - {self.title}"
        return self.get_order_type_display()

class EmployeeRelative(models.Model):

    RELATIONSHIP_CHOICES = [
        ("father", "پدر"),
        ("mother", "مادر"),
        ("brother", "برادر"),
        ("sister", "خواهر"),
        ("uncle_paternal", "عمو"),
        ("uncle_maternal", "دایی"),
        ("aunt_paternal", "عمه"),
        ("aunt_maternal", "خاله"),
        ("cousin", "پسرعمو/دخترعمو"),
        ("other", "سایر"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="relatives",
        verbose_name="پرسنل",
    )

    first_name = models.CharField(
        "نام",
        max_length=100,
    )

    last_name = models.CharField(
        "نام خانوادگی",
        max_length=100,
    )

    father_name = models.CharField(
        "نام پدر",
        max_length=100,
        blank=True,
    )

    relationship = models.CharField(
        "نسبت",
        max_length=30,
        choices=RELATIONSHIP_CHOICES,
    )


    position = models.CharField(
        "سمت",
        max_length=150,
        blank=True,
    )

    mobile = models.CharField(
        "شماره موبایل",
        max_length=20,
        blank=True,
    )

    class Meta:
        verbose_name = "بسته"
        verbose_name_plural = "بستگان"

    def __str__(self):
        return f"{self.get_relationship_display()} - {self.first_name} {self.last_name}"

class DeletedEmployeeDocument(EmployeeDocument):
    class Meta:
        proxy = True
        verbose_name = "مدرک حذف‌شده"
        verbose_name_plural = "مدارک حذف‌شده"
