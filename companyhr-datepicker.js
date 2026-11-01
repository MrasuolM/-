document.addEventListener("DOMContentLoaded", function () {

    const dateInputs = document.querySelectorAll(
        'input.vDateField[data-jdp]'
    );

    const persianDigits = "۰۱۲۳۴۵۶۷۸۹";
    const englishDigits = "0123456789";

    function toPersianDigits(value) {
        return String(value).replace(/[0-9]/g, function (digit) {
            return persianDigits[englishDigits.indexOf(digit)];
        });
    }

    dateInputs.forEach(function (input) {

        const originalName = input.name;

        if (!originalName) {
            return;
        }

        // مقدار اصلی میلادی که Django دریافت می‌کند
        const hiddenInput = document.createElement("input");

        hiddenInput.type = "hidden";
        hiddenInput.name = originalName;
        hiddenInput.id = originalName + "_gregorian";
        hiddenInput.value = input.value;

        // فیلد نمایشی جلالی
        input.name = originalName + "_jalali";

        input.setAttribute(
            "data-jdp-target-value-input",
            "#" + hiddenInput.id
        );

        input.setAttribute(
            "data-jdp-target-value-type",
            "gregorian"
        );

        input.parentNode.appendChild(hiddenInput);


        // تبدیل تاریخ موجود میلادی به جلالی
        if (hiddenInput.value) {

            const parts = hiddenInput.value.split("-");

            if (parts.length === 3) {

                const year = Number(parts[0]);
                const month = Number(parts[1]);
                const day = Number(parts[2]);

                const date = new Date(
                    year,
                    month - 1,
                    day
                );

                const formatter = new Intl.DateTimeFormat(
                    "en-US-u-ca-persian",
                    {
                        year: "numeric",
                        month: "2-digit",
                        day: "2-digit"
                    }
                );

                const dateParts = formatter.formatToParts(date);

                const jalaliYear =
                    dateParts.find(
                        part => part.type === "year"
                    ).value;

                const jalaliMonth =
                    dateParts.find(
                        part => part.type === "month"
                    ).value;

                const jalaliDay =
                    dateParts.find(
                        part => part.type === "day"
                    ).value;

                const jalaliDate =
                    jalaliYear.padStart(4, "0") +
                    "/" +
                    jalaliMonth.padStart(2, "0") +
                    "/" +
                    jalaliDay.padStart(2, "0");

                // نمایش فارسی
                input.value = toPersianDigits(jalaliDate);
            }
        }
    });


    // فعال کردن تقویم جلالی
    jalaliDatepicker.startWatch({
        targetValueInput: "attr",
        targetValueType: "attr",
        persianDigits: true
    });

});