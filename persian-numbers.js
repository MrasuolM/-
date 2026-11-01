(function () {

    const englishDigits = "0123456789";
    const persianDigits = "۰۱۲۳۴۵۶۷۸۹";


    function toPersianDigits(value) {

        return String(value).replace(/[0-9]/g, function (digit) {

            return persianDigits[
                englishDigits.indexOf(digit)
            ];

        });

    }


    function toEnglishDigits(value) {

        return String(value).replace(/[۰-۹]/g, function (digit) {

            return englishDigits[
                persianDigits.indexOf(digit)
            ];

        });

    }


    // ----------------------------------------
    // تبدیل اعداد معمولی صفحه به فارسی
    // ----------------------------------------

    function convertPageText() {

        document.querySelectorAll("body *").forEach(function (element) {

            if (
                element.matches(
                    "input, textarea, select, script, style"
                )
            ) {
                return;
            }

            element.childNodes.forEach(function (node) {

                if (node.nodeType === Node.TEXT_NODE) {

                    node.nodeValue =
                        toPersianDigits(node.nodeValue);

                }

            });

        });

    }


    // ----------------------------------------
    // سه فیلد عددی
    // ----------------------------------------

    const persianNumberFields = [
        "id_number",
        "passport_number",
        "children_count"
    ];


    function setupNumberInputs() {

        persianNumberFields.forEach(function (fieldName) {

            const input = document.querySelector(
                'input[name="' + fieldName + '"]'
            );


            if (!input) {
                return;
            }


            // جلوگیری از نصب دوباره
            if (input.dataset.persianReady === "true") {
                return;
            }


            // مقدار اولیه
            input.value =
                toPersianDigits(input.value);


            // هنگام تایپ
            input.addEventListener("input", function () {

                input.value =
                    toPersianDigits(input.value);

            });


            // هنگام خروج از فیلد
            input.addEventListener("blur", function () {

                input.value =
                    toPersianDigits(input.value);

            });


            // هنگام ارسال فرم
            const form = input.closest("form");

            if (form) {

                form.addEventListener("submit", function () {

                    input.value =
                        toEnglishDigits(input.value);

                });

            }


            input.dataset.persianReady = "true";

        });

    }


    // ----------------------------------------
    // اجرای اصلی
    // ----------------------------------------

    function startPersianNumbers() {

        convertPageText();

        setupNumberInputs();


        // اگر Django Admin بعداً فیلدها را ایجاد کرد
        const watcher = setInterval(function () {

            setupNumberInputs();

        }, 300);


        setTimeout(function () {

            clearInterval(watcher);

        }, 15000);

    }


    // ----------------------------------------
    // اجرای درست، حتی اگر DOMContentLoaded
    // قبلاً اتفاق افتاده باشد
    // ----------------------------------------

    if (document.readyState === "loading") {

        document.addEventListener(
            "DOMContentLoaded",
            startPersianNumbers
        );

    } else {

        startPersianNumbers();

    }


})();