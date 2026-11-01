from django.core.management.base import BaseCommand
from personnel.models import Province, City
import csv
import os


class Command(BaseCommand):

    help = "وارد کردن شهرهای واقعی ایران با اتصال صحیح به استان‌ها"

    def handle(self, *args, **options):

        # =====================================================
        # مسیر فایل شهرها
        # =====================================================

        file_path = os.path.join(
            "personnel",
            "data",
            "cities.csv"
        )

        if not os.path.exists(file_path):

            self.stdout.write(
                self.style.ERROR(
                    f"فایل پیدا نشد: {file_path}"
                )
            )

            return

        # =====================================================
        # نگاشت صحیح province_id فایل CSV
        # =====================================================

        province_map = {

            "100": "مرکزی",
            "101": "گیلان",
            "102": "مازندران",
            "103": "آذربایجان شرقی",
            "104": "آذربایجان غربی",
            "105": "کرمانشاه",
            "106": "خوزستان",
            "107": "فارس",
            "108": "کرمان",
            "109": "خراسان رضوی",
            "110": "اصفهان",
            "111": "سیستان و بلوچستان",
            "112": "کردستان",
            "113": "همدان",
            "114": "چهارمحال و بختیاری",
            "115": "لرستان",
            "116": "ایلام",
            "117": "کهگیلویه و بویراحمد",
            "118": "بوشهر",
            "119": "زنجان",
            "120": "سمنان",
            "121": "یزد",
            "122": "هرمزگان",
            "123": "تهران",
            "124": "اردبیل",
            "125": "قم",
            "126": "قزوین",
            "127": "گلستان",
            "128": "خراسان شمالی",
            "129": "خراسان جنوبی",
            "130": "البرز",
        }

        # =====================================================
        # حذف شهرهای قبلی
        # =====================================================

        deleted_count, _ = City.objects.all().delete()

        self.stdout.write(
            self.style.WARNING(
                f"{deleted_count} شهر قبلی حذف شد."
            )
        )

        # =====================================================
        # شمارنده‌ها
        # =====================================================

        created_count = 0
        skipped_count = 0

        # =====================================================
        # خواندن CSV
        # =====================================================

        with open(
            file_path,
            "r",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                province_id = row["province_id"].strip()
                city_name = row["name"].strip()

                # پیدا کردن نام استان
                province_name = province_map.get(
                    province_id
                )

                if not province_name:

                    skipped_count += 1

                    self.stdout.write(
                        self.style.WARNING(
                            f"شناسه استان ناشناخته: "
                            f"{province_id} - {city_name}"
                        )
                    )

                    continue

                # پیدا کردن استان در دیتابیس
                try:

                    province = Province.objects.get(
                        name=province_name
                    )

                except Province.DoesNotExist:

                    skipped_count += 1

                    self.stdout.write(
                        self.style.WARNING(
                            f"استان در دیتابیس پیدا نشد: "
                            f"{province_name}"
                        )
                    )

                    continue

                # ایجاد شهر
                city, created = City.objects.get_or_create(
                    province=province,
                    name=city_name
                )

                if created:
                    created_count += 1
                else:
                    skipped_count += 1

        # =====================================================
        # نتیجه نهایی
        # =====================================================

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                f"{created_count} شهر ایجاد شد."
            )
        )

        self.stdout.write(
            f"{skipped_count} مورد قبلاً وجود داشت یا رد شد."
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "عملیات ورود شهرها با موفقیت پایان یافت."
            )
        )