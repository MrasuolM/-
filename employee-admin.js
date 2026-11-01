document.addEventListener("DOMContentLoaded", function () {

    console.log("CompanyHR employee-admin.js loaded");


    // =========================================================
    // ابزارهای عمومی
    // =========================================================

    function getFieldsetByTitle(titleText) {
        return Array.from(
            document.querySelectorAll("#content-main fieldset")
        ).find(function (fieldset) {
            const title = fieldset.querySelector("h2");
            return title && title.textContent.trim() === titleText;
        });
    }


    function showRow(row) {
        if (row) row.style.display = "";
    }


    function hideRow(row) {
        if (row) row.style.display = "none";
    }


    // =========================================================
    // پیدا کردن بخش‌های Inline
    // =========================================================

    const mobileInline =
        document.querySelector("#mobile_numbers-group") ||
        document.querySelector("#employeemobile_set-group");

    const addressGroup =
        document.querySelector("#addresses-group") ||
        document.querySelector("#employeeaddress_set-group");

    const familyGroup =
        document.querySelector("#family_members-group") ||
        document.querySelector("#employeefamilymember_set-group");


    // =========================================================
    // اطلاعات تماس
    // =========================================================

    const contactFieldset = getFieldsetByTitle("اطلاعات تماس");

    if (contactFieldset && mobileInline) {
        const mobileTitle = mobileInline.querySelector("h2");
        if (mobileTitle) mobileTitle.style.display = "none";

        const landlineRow = contactFieldset.querySelector(".form-row.field-landline");
        const emailRow = contactFieldset.querySelector(".form-row.field-personal_email");

        contactFieldset.appendChild(mobileInline);
        if (landlineRow) contactFieldset.appendChild(landlineRow);
        if (emailRow) contactFieldset.appendChild(emailRow);
    }


    // =========================================================
    // استان و شهر
    // =========================================================

    function loadCities(provinceSelect, citySelect, selectedCityId = "") {
        const provinceId = provinceSelect.value;
        citySelect.innerHTML = "";

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "انتخاب کنید";
        citySelect.appendChild(defaultOption);

        if (!provinceId) return;

        fetch(`/personnel/cities-by-province/?province_id=${provinceId}`)
            .then(function (response) {
                if (!response.ok) throw new Error("خطا در دریافت شهرها");
                return response.json();
            })
            .then(function (cities) {
                cities.forEach(function (city) {
                    const option = document.createElement("option");
                    option.value = city.id;
                    option.textContent = city.name;
                    if (String(city.id) === String(selectedCityId)) {
                        option.selected = true;
                    }
                    citySelect.appendChild(option);
                });
            })
            .catch(function (error) {
                console.error("خطا در دریافت شهرها:", error);
            });
    }


    function setupAddressRow(row) {
        if (!row) return;

        const provinceSelect = row.querySelector('select[name$="-province"]');
        const citySelect = row.querySelector('select[name$="-city"]');
        if (!provinceSelect || !citySelect) return;

        const currentCityId = citySelect.value;

        provinceSelect.addEventListener("change", function () {
            loadCities(provinceSelect, citySelect);
        });

        if (provinceSelect.value) {
            loadCities(provinceSelect, citySelect, currentCityId);
        }
    }


    if (addressGroup) {
        addressGroup.querySelectorAll(".inline-related").forEach(function (row) {
            setupAddressRow(row);
        });
    }


    // =========================================================
    // رفتار اطلاعات هویتی
    // =========================================================

    function setupIdentityBehavior() {
        const identityFieldset =
            document.querySelector('.companyhr-section-title')
            ?.closest('.companyhr-section');

        if (!identityFieldset) return;

        const idType = identityFieldset.querySelector('[name="id_type"]');
        const idIssueDateRow = identityFieldset.querySelector(".form-row.field-id_issue_date");
        const duplicateIssueDateRow = identityFieldset.querySelector(".form-row.field-duplicate_issue_date");
        const duplicateReasonRow = identityFieldset.querySelector(".form-row.field-duplicate_issue_reason");

        function updateIdType() {
            if (!idType) return;
            if (idType.value === "original") {
                showRow(idIssueDateRow);
                hideRow(duplicateIssueDateRow);
                hideRow(duplicateReasonRow);
            } else if (idType.value === "duplicate") {
                hideRow(idIssueDateRow);
                showRow(duplicateIssueDateRow);
                showRow(duplicateReasonRow);
            } else {
                showRow(idIssueDateRow);
                hideRow(duplicateIssueDateRow);
                hideRow(duplicateReasonRow);
            }
        }

        if (idType) {
            idType.addEventListener("change", updateIdType);
            updateIdType();
        }

        const gender = identityFieldset.querySelector('[name="gender"]');
        const militaryStatusRow = identityFieldset.querySelector(".form-row.field-military_status");
        const militaryExplanationRow = identityFieldset.querySelector(".form-row.field-military_explanation");

        function updateGender() {
            if (!gender) return;
            if (gender.value === "female") {
                hideRow(militaryStatusRow);
                hideRow(militaryExplanationRow);
            } else {
                showRow(militaryStatusRow);
                showRow(militaryExplanationRow);
            }
        }

        if (gender) {
            gender.addEventListener("change", updateGender);
            updateGender();
        }

        const maritalStatus = identityFieldset.querySelector('[name="marital_status"]');
        const childrenCountRow = identityFieldset.querySelector(".form-row.field-children_count");

        function updateMaritalStatus() {
            if (!maritalStatus) return;
            if (maritalStatus.value === "single") {
                hideRow(childrenCountRow);
            } else {
                showRow(childrenCountRow);
            }
        }

        if (maritalStatus) {
            maritalStatus.addEventListener("change", updateMaritalStatus);
            updateMaritalStatus();
        }

        const dualNationality = identityFieldset.querySelector('[name="has_dual_nationality"]');
        const secondNationalityRow = identityFieldset.querySelector(".form-row.field-second_nationality");

        function updateDualNationality() {
            if (!dualNationality) return;
            if (dualNationality.checked) {
                showRow(secondNationalityRow);
            } else {
                hideRow(secondNationalityRow);
            }
        }

        if (dualNationality) {
            dualNationality.addEventListener("change", updateDualNationality);
            updateDualNationality();
        }

        const passportType = identityFieldset.querySelector('[name="passport_type"]');
        const passportNumberRow = identityFieldset.querySelector(".form-row.field-passport_number");
        const passportIssueDateRow = identityFieldset.querySelector(".form-row.field-passport_issue_date");

        function updatePassport() {
            if (!passportType) return;
            if (passportType.value === "none" || passportType.value === "") {
                hideRow(passportNumberRow);
                hideRow(passportIssueDateRow);
            } else {
                showRow(passportNumberRow);
                showRow(passportIssueDateRow);
            }
        }

        if (passportType) {
            passportType.addEventListener("change", updatePassport);
            updatePassport();
        }
    }


    // =========================================================
    // رفتار اطلاعات استخدامی
    // =========================================================

    function setupEmploymentBehavior() {
        const employmentSection = Array.from(
            document.querySelectorAll(".companyhr-section")
        ).find(function (sec) {
            const t = sec.querySelector("h2");
            return t && t.textContent.trim() === "اطلاعات استخدامی";
        });

        if (!employmentSection) return;

        const employmentStatus = employmentSection.querySelector('[name="employment_status"]');
        const suspensionStartRow = employmentSection.querySelector(".form-row.field-suspension_start_date");
        const suspensionEndRow = employmentSection.querySelector(".form-row.field-suspension_end_date");
        const terminationDateRow = employmentSection.querySelector(".form-row.field-termination_date");
        const terminationReasonRow = employmentSection.querySelector(".form-row.field-termination_reason");
        const retirementDateRow = employmentSection.querySelector(".form-row.field-retirement_date");

        function updateEmploymentStatus() {
            if (!employmentStatus) return;
            const value = employmentStatus.value;

            if (value === "active") {
                hideRow(suspensionStartRow);
                hideRow(suspensionEndRow);
                hideRow(terminationDateRow);
                hideRow(terminationReasonRow);
                hideRow(retirementDateRow);
            } else if (value === "suspended") {
                showRow(suspensionStartRow);
                showRow(suspensionEndRow);
                hideRow(terminationDateRow);
                hideRow(terminationReasonRow);
                hideRow(retirementDateRow);
            } else if (value === "terminated") {
                hideRow(suspensionStartRow);
                hideRow(suspensionEndRow);
                showRow(terminationDateRow);
                showRow(terminationReasonRow);
                hideRow(retirementDateRow);
            } else if (value === "retired") {
                hideRow(suspensionStartRow);
                hideRow(suspensionEndRow);
                hideRow(terminationDateRow);
                hideRow(terminationReasonRow);
                showRow(retirementDateRow);
            } else {
                hideRow(suspensionStartRow);
                hideRow(suspensionEndRow);
                hideRow(terminationDateRow);
                hideRow(terminationReasonRow);
                hideRow(retirementDateRow);
            }
        }

        if (employmentStatus) {
            employmentStatus.addEventListener("change", updateEmploymentStatus);
            updateEmploymentStatus();
        }
    }


    // =========================================================
    // تبدیل تاریخ میلادی به جلالی
    // =========================================================

    function gregorianToJalali(inputValue) {
        const parts = inputValue.split("-");
        if (parts.length !== 3) return "";

        const year = Number(parts[0]);
        const month = Number(parts[1]);
        const day = Number(parts[2]);

        if (!(year > 1900 && year < 2100 && month >= 1 && month <= 12)) {
            return "";
        }

        const date = new Date(year, month - 1, day);
        const formatter = new Intl.DateTimeFormat(
            "en-US-u-ca-persian",
            { year: "numeric", month: "2-digit", day: "2-digit" }
        );
        const dateParts = formatter.formatToParts(date);

        const jy = dateParts.find(p => p.type === "year").value.padStart(4, "0");
        const jm = dateParts.find(p => p.type === "month").value.padStart(2, "0");
        const jd = dateParts.find(p => p.type === "day").value.padStart(2, "0");

        return jy + "/" + jm + "/" + jd;
    }


    // =========================================================
    // آماده‌سازی input تاریخ خانواده
    // =========================================================

    function prepareFamilyDateInput(input) {

        if (!input) return;
        if (input.dataset.dateReady === "true") return;

        const originalName = input.name;
        if (!originalName) return;

        if (originalName.endsWith("_jalali")) {
            input.dataset.dateReady = "true";
            return;
        }

        input.classList.add("vDateField");
        input.setAttribute("autocomplete", "off");
        input.setAttribute("data-jdp", "");
        input.setAttribute("placeholder", "مثلاً ۱۴۰۵/۰۱/۱۵");

        const hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.name = originalName;
        hiddenInput.id = originalName + "_gregorian";
        hiddenInput.value = input.value || "";

        input.name = originalName + "_jalali";
        input.setAttribute(
            "data-jdp-target-value-input",
            "#" + hiddenInput.id
        );
        input.setAttribute("data-jdp-target-value-type", "gregorian");

        input.parentNode.appendChild(hiddenInput);

        if (hiddenInput.value) {
            const jalali = gregorianToJalali(hiddenInput.value);
            if (jalali) {
                input.value = jalali;
            }
        }

        input.dataset.dateReady = "true";
    }


    function prepareFamilyDates(row) {
        if (!row) return;
        prepareFamilyDateInput(row.querySelector('input[name$="-birth_date"]'));
        prepareFamilyDateInput(row.querySelector('input[name$="-marriage_date"]'));
        prepareFamilyDateInput(row.querySelector('input[name$="-divorce_date"]'));
    }


    // =========================================================
    // رفتار نسبت اعضای خانواده
    // =========================================================

    function updateFamilyRelationship(row) {
        if (!row) return;

        const relationshipSelect = row.querySelector('select[name$="-relationship"]');
        if (!relationshipSelect) return;

        const marriageRow = row.querySelector(".form-row.field-marriage_date");
        const divorceRow = row.querySelector(".form-row.field-divorce_date");
        if (!marriageRow || !divorceRow) return;

        const relationship = relationshipSelect.value;

        if (relationship === "current_spouse" || relationship === "second_spouse") {
            showRow(marriageRow);
            hideRow(divorceRow);
            return;
        }

        if (relationship === "former_spouse") {
            hideRow(marriageRow);
            showRow(divorceRow);
            return;
        }

        hideRow(marriageRow);
        hideRow(divorceRow);
    }


    function setupFamilyRow(row) {
        if (!row) return;

        prepareFamilyDates(row);
        updateFamilyRelationship(row);

        const relationshipSelect = row.querySelector('select[name$="-relationship"]');
        if (relationshipSelect) {
            relationshipSelect.addEventListener("change", function () {
                updateFamilyRelationship(row);
            });
        }
    }


    if (familyGroup) {
        familyGroup.querySelectorAll(".inline-related").forEach(function (row) {
            setupFamilyRow(row);
        });
    }


    // =========================================================
    // Inline جدید
    // =========================================================

    document.addEventListener("formset:added", function (event) {
        const row = event.target;
        if (!row) return;

        if (row.querySelector && row.querySelector('select[name$="-province"]')) {
            setupAddressRow(row);
        }

        if (row.querySelector && row.querySelector('select[name$="-relationship"]')) {
            setupFamilyRow(row);
        }

        if (row.querySelector && row.querySelector('select[name$="-document_type"]')) {
            setTimeout(updateAllDocumentRows, 50);
        }
    });


    // =========================================================
    // اسناد پیوست — نمایش شرطی سطح مدرک
    // =========================================================

    function updateAllDocumentRows() {
        const docGroup = document.querySelector("#documents-group");
        if (!docGroup) return;

        docGroup.querySelectorAll("tr.form-row").forEach(function (row) {
            const typeSelect = row.querySelector('select[name$="-document_type"]');
            if (!typeSelect) return;

            const eduCell = row.querySelector("td.field-education_level");
            if (!eduCell) return;

            if (typeSelect.value === "education") {
                eduCell.style.display = "";
            } else {
                eduCell.style.display = "none";
            }
        });

        let hasEducation = false;
        docGroup.querySelectorAll('tr.form-row select[name$="-document_type"]').forEach(function (s) {
            if (s.value === "education") hasEducation = true;
        });

        const th = docGroup.querySelector("th.column-education_level");
        if (th) {
            th.style.display = hasEducation ? "" : "none";
        }
    }


    document.addEventListener("change", function (event) {
        if (
            event.target.matches &&
            event.target.matches('#documents-group select[name$="-document_type"]')
        ) {
            updateAllDocumentRows();
        }
    });


    // =========================================================
    // کشویی کردن اعضای خانواده و بستگان و معرف
    // =========================================================

    function setupFamilyCollapse() {
        document.addEventListener("click", function (event) {

            const selectors = [
                "#family_members-group .inline-related > h3",
                "#relatives-group .inline-related > h3",
                "#referrer-group .inline-related > h3",
            ];

            let heading = null;
            for (let i = 0; i < selectors.length; i++) {
                heading = event.target.closest(selectors[i]);
                if (heading) break;
            }

            if (!heading) return;

            if (event.target.closest("a.delete, a.inline-delete, .delete, .inline-deletelink, input[type=checkbox], button")) {
                return;
            }

            const row = heading.closest(".inline-related");
            if (!row) return;

            row.classList.toggle("collapsed");
        });
    }


    // =========================================================
    // هشدار قبل از حذف
    // =========================================================

    function setupDeleteWarning() {

        document.addEventListener("change", function (event) {
            const checkbox = event.target;
            if (!checkbox.matches) return;
            if (!checkbox.matches('input[type="checkbox"][name$="-DELETE"]')) return;

            if (checkbox.checked) {
                const confirmed = confirm(
                    "⚠️ آیا مطمئن هستید؟\n\n" +
                    "این مورد از لیست حذف می‌شود.\n" +
                    "اطلاعات در پایگاه داده باقی می‌ماند و " +
                    "توسط مدیر ارشد قابل مشاهده است."
                );

                if (!confirmed) {
                    checkbox.checked = false;
                }
            }
        });

        document.addEventListener("click", function (event) {
            const link = event.target.closest(
                "a.deletelink, a.delete, a.inline-deletelink"
            );

            if (!link) return;

            const confirmed = confirm(
                "⚠️ آیا مطمئن هستید؟\n\n" +
                "این مورد از لیست حذف می‌شود.\n" +
                "اطلاعات در پایگاه داده باقی می‌ماند."
            );

            if (!confirmed) {
                event.preventDefault();
                event.stopPropagation();
                return false;
            }
        });
    }


    // =========================================================
    // هشدار خروج بدون ذخیره
    // =========================================================

    function setupUnsavedWarning() {
        const form = document.querySelector("#employee_form");
        if (!form) return;

        let isDirty = false;
        let isSubmitting = false;

        form.addEventListener("input", function () { isDirty = true; });
        form.addEventListener("change", function () { isDirty = true; });
        form.addEventListener("submit", function () {
            isSubmitting = true;
            isDirty = false;
        });

        window.addEventListener("beforeunload", function (e) {
            if (isDirty && !isSubmitting) {
                const msg = "همکار محترم، تغییراتی که انجام داده‌اید ذخیره نشده است";
                e.preventDefault();
                e.returnValue = msg;
                return msg;
            }
        });
    }


    // =========================================================
    // حالت نمایش/ویرایش — برای همه Inline ها
    // =========================================================

    function setupAllInlinesViewEditMode() {

        const groups = [
            { id: "orders-group", type: "tabular" },
            { id: "mobile_numbers-group", type: "tabular" },
            { id: "addresses-group", type: "tabular" },
            { id: "relatives-group", type: "stacked" },
            { id: "family_members-group", type: "stacked" },
            { id: "referrer-group", type: "stacked" },
        ];

        groups.forEach(function (cfg) {
            const group = document.getElementById(cfg.id);
            if (!group) return;

            const rows = cfg.type === "stacked"
                ? group.querySelectorAll(".inline-related:not(.empty-form)")
                : group.querySelectorAll("tr.form-row");

            rows.forEach(function (row) {
                const idInput = row.querySelector('input[name$="-id"]');
                const hasId = idInput && idInput.value && idInput.value !== "";
                if (!hasId) return;

                if (cfg.type === "stacked") {
                    applyStackedViewMode(row);
                } else {
                    applyTabularViewMode(row);
                }
            });
        });
    }


    // ─────────── Tabular ───────────

    function applyTabularViewMode(row) {
        if (row.dataset.viewReady === "true") return;
        row.dataset.viewReady = "true";
        row.classList.add("inline-view-mode");

        addCollapseToggle(row);

        row.querySelectorAll("td").forEach(function (cell) {
            if (cell.classList.contains("original") || cell.classList.contains("delete")) return;

            const input = cell.querySelector(
                'input:not([type=hidden]):not([type=checkbox]), select, textarea'
            );
            if (!input) return;

            const text = extractDisplayText(cell, input);

            const span = document.createElement("span");
            span.className = "inline-view-text";
            span.textContent = text;

            cell.appendChild(span);
        });

        addTabularEditButton(row);
    }


    function extractDisplayText(cell, input) {
        let text = "";

        if (input.tagName === "SELECT") {
            const opt = input.options[input.selectedIndex];
            text = opt ? opt.text.trim() : "";
        } else if (input.type === "file") {
            const link = cell.querySelector("a[href]");
            text = link
                ? "📎 " + (link.textContent.trim() || "فایل")
                : "— بدون فایل —";
        } else {
            text = input.value || "";
        }

        if (!text ||
            text === "---------" ||
            text === "- Select an option -" ||
            text === "انتخاب کنید") {
            text = "—";
        }

        return text;
    }


    function addCollapseToggle(row) {
        const firstCell = row.querySelector("td.original");
        if (!firstCell || firstCell.querySelector(".inline-collapse-btn")) return;

        const btn = document.createElement("span");
        btn.className = "inline-collapse-btn";
        btn.textContent = "▼";
        btn.title = "بستن/باز کردن";

        btn.addEventListener("click", function (e) {
            e.preventDefault();
            row.classList.toggle("inline-collapsed");
            btn.textContent = row.classList.contains("inline-collapsed") ? "◀" : "▼";
        });

        firstCell.appendChild(btn);
    }


    function addTabularEditButton(row) {
        const deleteCell = row.querySelector("td.delete");
        if (!deleteCell || deleteCell.querySelector(".inline-edit-btn")) return;

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "inline-edit-btn";
        btn.textContent = "✎ ویرایش";

        btn.addEventListener("click", function (e) {
            e.preventDefault();
            toggleRowEditMode(row, "tabular");
        });

        deleteCell.appendChild(btn);
    }


    // ─────────── Stacked ───────────

    function applyStackedViewMode(row) {
        if (row.dataset.viewReady === "true") return;
        row.dataset.viewReady = "true";
        row.classList.add("inline-view-mode-stacked");

        // داخل هر form-row
        row.querySelectorAll(".form-row").forEach(function (formRow) {

            const input = formRow.querySelector(
                'input:not([type=hidden]):not([type=checkbox]), select, textarea'
            );
            if (!input) return;

            const text = extractDisplayText(formRow, input);

            const span = document.createElement("span");
            span.className = "inline-view-text";
            span.textContent = text;

            const box = formRow.querySelector(".field-box") || input.parentNode;
            box.appendChild(span);
        });

        addStackedEditButton(row);
    }


    function addStackedEditButton(row) {
        const h3 = row.querySelector(":scope > h3");
        if (!h3 || h3.querySelector(".inline-edit-btn")) return;

        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "inline-edit-btn";
        btn.textContent = "✎ ویرایش";

        btn.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            toggleRowEditMode(row, "stacked");
        });

        h3.appendChild(btn);
    }


    // ─────────── مشترک ───────────

    function toggleRowEditMode(row, type) {
        const viewClass = type === "stacked"
            ? "inline-view-mode-stacked"
            : "inline-view-mode";

        const isViewMode = row.classList.contains(viewClass);

        if (isViewMode) {
            row.classList.remove(viewClass);
            const btn = row.querySelector(".inline-edit-btn");
            if (btn) {
                btn.textContent = "✕ انصراف";
                btn.classList.add("inline-edit-btn-cancel");
            }
        } else {
            row.classList.add(viewClass);
            const btn = row.querySelector(".inline-edit-btn");
            if (btn) {
                btn.textContent = "✎ ویرایش";
                btn.classList.remove("inline-edit-btn-cancel");
            }
        }
    }

    

    // =========================================================
    // منوی هایپرلینک برای اسناد پیوست
    // =========================================================

    function setupDocumentHyperlinkMenu() {

        const docGroup = document.querySelector("#documents-group");
        if (!docGroup) return;

        // ۱. افزودن عنوان گروه «اسناد»
        if (!docGroup.querySelector(".doc-menu-header")) {
            const header = document.createElement("div");
            header.className = "doc-menu-header";
            header.textContent = "اسناد پیوست";
            docGroup.insertBefore(header, docGroup.firstChild);
        }

        // ۲. هر ردیف → یک لینک
        docGroup.querySelectorAll("tr.form-row").forEach(function (row) {

            const idInput = row.querySelector('input[name$="-id"]');
            const hasId = idInput && idInput.value && idInput.value !== "";
            if (!hasId) return;

            // ردیف بسته باشه
            row.classList.add("doc-collapsed");

            const typeCell = row.querySelector("td.field-document_type");
            if (!typeCell ) return;

            
            typeCell.classList.add("doc-type-link");
            typeCell.title = "کلیک برای نمایش جزئیات";

            // ★★★ پیدا کردن select و مخفی کردنش ★★★
            const selectEl = typeCell.querySelector("select");
            if (selectEl) {
                selectEl.style.display = "none";
                selectEl.setAttribute("data-hidden-by-hyperlink", "true");
            }

            // ★★★ پیدا کردن متن نمایشی (اگه موجود باشه) ★★★
            // اگه روی ردیف حالت View Mode اعمال شده، متن رو از span بگیر
            let displayText = "";

            // اول از select بگیر
            if (selectEl) {
                const opt = selectEl.options[selectEl.selectedIndex];
                displayText = opt ? opt.text.trim() : "";
            }

            // اگه از select نگرفتیم، از متن سلول بگیر
            if (!displayText) {
                const span = typeCell.querySelector(".inline-view-text, .doc-view-text");
                if (span) {
                    displayText = span.textContent.trim();
                }
            }

            // اگه بازم خالی، از متن سلول بخون
            if (!displayText) {
                displayText = typeCell.textContent.trim();
            }

            if (!displayText || displayText === "---------") {
                displayText = "—";
            }

            // ★★★ پاک کردن محتوای سلول و جایگزینی با هایپرلینک ★★★
            typeCell.innerHTML = "";

            // فلش
            const arrow = document.createElement("span");
            arrow.className = "doc-type-arrow";
            arrow.textContent = "◀";
            typeCell.appendChild(arrow);

            // متن هایپرلینک
            const linkSpan = document.createElement("span");
            linkSpan.className = "doc-type-text";
            linkSpan.textContent = displayText;
            typeCell.appendChild(linkSpan);

            // ★★★ رویداد کلیک ★★★
            typeCell.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopPropagation();

                row.classList.toggle("doc-collapsed");

                arrow.textContent = row.classList.contains("doc-collapsed") ? "◀" : "▼";
            });
        });
    }

    // =========================================================
    // ساخت تب‌های پرونده
    // =========================================================

    function buildEmployeeTabs() {
        const contentMain = document.querySelector("#content-main");
        if (!contentMain) return;
        if (document.querySelector(".companyhr-tabs")) return;

        const mainFieldset = document.querySelector("#employee_form > div > fieldset");
        if (!mainFieldset) {
            console.log("fieldset اصلی فرم پیدا نشد.");
            return;
        }

        const referrerGroup =
            document.querySelector("#employeereferrer_set-group") ||
            document.querySelector("#referrer-group");

        const mobileInlineLocal =
            document.querySelector("#mobile_numbers-group") ||
            document.querySelector("#employeemobile_set-group");

        const addressGroupLocal =
            document.querySelector("#addresses-group") ||
            document.querySelector("#employeeaddress_set-group");

        const familyGroupLocal =
            document.querySelector("#family_members-group") ||
            document.querySelector("#employeefamilymember_set-group");

        const rows = Array.from(mainFieldset.querySelectorAll(":scope > .form-row"));
        const rowByField = {};

        rows.forEach(function (row) {
            const className = Array.from(row.classList).find(function (cls) {
                return cls.startsWith("field-");
            });
            if (className) {
                const fieldName = className.replace("field-", "");
                rowByField[fieldName] = row;
            }
        });

        const identityFields = [
            "first_name", "last_name", "national_code",
            "birth_certificate_serial", "bank_account_status",
            "father_name", "previous_last_name", "nickname",
            "birth_date", "birth_place",
            "id_number", "id_issue_place", "id_type", "id_issue_date",
            "duplicate_issue_date", "duplicate_issue_reason",
            "gender", "marital_status", "children_count",
            "religion", "nationality", "has_dual_nationality", "second_nationality",
            "education_level", "field_of_study",
            "passport_type", "passport_number", "passport_issue_date",
            "military_status", "military_explanation",
            "photo"
            
        ];

        const contactFields = ["landline", "personal_email"];

        const employmentFields = [
            "personnel_code", "hire_date", "employment_status",
            "suspension_start_date", "suspension_end_date",
            "termination_date", "termination_reason", "retirement_date",
            "department", "position",
            "employment_type", "current_position_start_date",
            "employment_notes"
        ];

        function createSection(title, fields) {
            const section = document.createElement("div");
            section.className = "companyhr-section";

            const titleElement = document.createElement("h2");
            titleElement.textContent = title;
            titleElement.className = "companyhr-section-title";
            section.appendChild(titleElement);

            fields.forEach(function (fieldName) {
                const row = rowByField[fieldName];
                if (row) section.appendChild(row);
            });

            return section;
        }

        const identitySection = createSection("اطلاعات هویتی", identityFields);
        const contactSection = createSection("اطلاعات تماس", contactFields);
        const employmentSection = createSection("اطلاعات استخدامی", employmentFields);

        const documentsGroup = document.querySelector("#documents-group");
        if (documentsGroup) identitySection.appendChild(documentsGroup);

        const ordersGroup = document.querySelector("#orders-group");
        if (ordersGroup) employmentSection.appendChild(ordersGroup);

        const relativesGroup = document.querySelector("#relatives-group");
        if (relativesGroup) employmentSection.appendChild(relativesGroup);

        const tabsContainer = document.createElement("div");
        tabsContainer.className = "companyhr-tabs";

        const tabButtons = document.createElement("div");
        tabButtons.className = "companyhr-tab-buttons";

        const tabContents = document.createElement("div");
        tabContents.className = "companyhr-tab-contents";

        const tabs = [
            { id: "identity", title: "اطلاعات هویتی", element: identitySection },
            { id: "contact", title: "اطلاعات تماس", element: contactSection, extraElement: mobileInlineLocal },
            { id: "address", title: "اطلاعات آدرس", element: addressGroupLocal },
            { id: "employment", title: "اطلاعات استخدامی", element: employmentSection, extraElement: referrerGroup },
            { id: "family", title: "اطلاعات خانواده", element: familyGroupLocal }
        ];

        tabs.forEach(function (tab, index) {
            if (!tab.element) return;

            const button = document.createElement("button");
            button.type = "button";
            button.className = "companyhr-tab-button";
            button.textContent = tab.title;
            button.dataset.tab = tab.id;

            const panel = document.createElement("div");
            panel.className = "companyhr-tab-panel";
            panel.dataset.panel = tab.id;

            if (tab.id === "contact" && tab.extraElement) {
                panel.appendChild(tab.extraElement);
                panel.appendChild(tab.element);
            } else {
                panel.appendChild(tab.element);
                if (tab.extraElement) {
                    panel.appendChild(tab.extraElement);
                }
            }

            if (index === 0) {
                button.classList.add("active");
                panel.classList.add("active");
            }

            button.addEventListener("click", function () {
                document.querySelectorAll(".companyhr-tab-button").forEach(function (btn) {
                    btn.classList.remove("active");
                });
                document.querySelectorAll(".companyhr-tab-panel").forEach(function (content) {
                    content.classList.remove("active");
                });
                button.classList.add("active");
                panel.classList.add("active");
            });

            tabButtons.appendChild(button);
            tabContents.appendChild(panel);
        });

        tabsContainer.appendChild(tabButtons);
        tabsContainer.appendChild(tabContents);

        const form = document.querySelector("#employee_form");
        if (form) {
            form.prepend(tabsContainer);
        } else {
            contentMain.prepend(tabsContainer);
        }

        console.log("تب‌های پرونده پرسنل ساخته شدند.");
    }


    // =====================================================
    // کارت خلاصه پرونده پرسنل
    // =====================================================

    let employeePhotoPreviewUrl = null;

    

function buildEmployeeSummaryCard() {
    const contentMain = document.querySelector("#content-main");
    const employeeForm = document.querySelector("#employee_form");

    if (!contentMain || !employeeForm) return;

    let card = document.querySelector(".companyhr-summary-card");

    if (!card) {
        card = document.createElement("section");
        card.className = "companyhr-summary-card";
        card.setAttribute("dir", "rtl");
        card.setAttribute("aria-label", "خلاصه پرونده پرسنل");
    }

    function getValue(name) {
        const field = employeeForm.querySelector(
            `[name="${name}"]`
        );

        if (!field) return "—";

        if (field.tagName === "SELECT") {
            return field.selectedOptions[0]?.textContent.trim() || "—";
        }

        return field.value?.trim() || "—";
    }

    // تبدیل اعداد انگلیسی به فارسی
    function toPersianDigits(value) {
        return String(value).replace(
            /\d/g,
            digit => "۰۱۲۳۴۵۶۷۸۹"[Number(digit)]
        );
    }

    // نمایش تاریخ میلادی ذخیره‌شده به شکل شمسی
    function formatPersianDate(value) {
        if (!value || value === "—") {
            return "ثبت نشده";
        }

        // تاریخ باید در قالب YYYY-MM-DD باشد.
        const jalaliDate = gregorianToJalali(value);

        if (!jalaliDate) {
            return "ثبت نشده";
        }

        return toPersianDigits(jalaliDate);
    }

    function setText(selector, value) {
        const element = card.querySelector(selector);
        if (element) element.textContent = value || "—";
    }

    const firstName = getValue("first_name");
    const lastName = getValue("last_name");

    const fullName = [firstName, lastName]
        .filter(value => value !== "—")
        .join(" ");

    const photoInput = employeeForm.querySelector(
        'input[type="file"][name="photo"]'
    );

    const photoRow = photoInput?.closest(".form-row");
    const existingPhotoLink = photoRow?.querySelector("a[href]");

    let photoUrl = "";

    if (photoInput?.files?.length) {
        if (employeePhotoPreviewUrl) {
            URL.revokeObjectURL(employeePhotoPreviewUrl);
        }

        employeePhotoPreviewUrl = URL.createObjectURL(
            photoInput.files[0]
        );

        photoUrl = employeePhotoPreviewUrl;
    } else if (existingPhotoLink) {
        photoUrl = existingPhotoLink.href;
    }

    card.innerHTML = `
        <div class="companyhr-summary-main">
            <div class="companyhr-summary-photo">
                <img class="companyhr-summary-photo-img"
                     alt="عکس پرسنلی"
                     hidden>
                <span class="companyhr-summary-photo-placeholder">
                    👤
                </span>
            </div>

            <div class="companyhr-summary-identity">
                <div class="companyhr-summary-eyebrow">
                    خلاصه پرونده پرسنل
                </div>

                <h2 class="companyhr-summary-name"></h2>

                <div class="companyhr-summary-code">
                    کد پرسنلی:
                    <strong class="summary-personnel-code"></strong>
                </div>

                <span class="companyhr-summary-status"></span>
            </div>
        </div>

        <div class="companyhr-summary-details">
            <div class="companyhr-summary-item">
                <span>واحد سازمانی</span>
                <strong class="summary-department"></strong>
            </div>

            <div class="companyhr-summary-item">
                <span>سمت</span>
                <strong class="summary-position"></strong>
            </div>

            <div class="companyhr-summary-item">
                <span>تاریخ استخدام</span>
                <strong class="summary-hire-date"></strong>
            </div>

            <div class="companyhr-summary-item">
                <span>تاریخ تولد</span>
                <strong class="summary-birth-date"></strong>
            </div>

            <div class="companyhr-summary-item">
                <span>شماره تماس</span>
                <strong class="summary-phone"></strong>
            </div>

            <div class="companyhr-summary-item">
                 <span>وضعیت شماره حساب</span>
                 <strong class="summary-bank-account-status"></strong>
            </div>
        </div>


        <div class="companyhr-summary-documents">
            <div class="companyhr-summary-doc-item">
                <span class="summary-doc-present">۰</span>
                <span>نوع مدرک موجود</span>
            </div>

            <div class="companyhr-summary-doc-item is-missing">
                <span class="summary-doc-missing">۰</span>
                <span>نوع مدرک ناقص</span>
            </div>
        </div>
    `;

    setText(".companyhr-summary-name", fullName || "کارمند جدید");
    setText(
        ".summary-personnel-code",
        toPersianDigits(getValue("personnel_code"))
    );
    setText(".summary-department", getValue("department"));
    setText(".summary-position", getValue("position"));

    setText(
        ".summary-hire-date",
        formatPersianDate(getValue("hire_date"))
    );

    setText(
        ".summary-birth-date",
        formatPersianDate(getValue("birth_date"))
    );

    setText(
        ".summary-phone",
        toPersianDigits(getValue("phone"))
    );

const bankAccountField = employeeForm.querySelector(
    '[name="bank_account_status"]'
);

const bankAccountElement = card.querySelector(
    ".summary-bank-account-status"
);

 function updateBankAccountSummary() {
    if (!bankAccountField || !bankAccountElement) return;

    const value = bankAccountField.value;

    bankAccountElement.textContent =
        value === "yes" ? "دارد" :
        value === "no" ? "ندارد" :
        "ثبت نشده";

    bankAccountElement.classList.toggle(
        "bank-account-yes",
        value === "yes"
    );

    bankAccountElement.classList.toggle(
        "bank-account-no",
        value === "no"
    );
}

if (bankAccountField) {
    bankAccountField.removeEventListener(
        "change",
        updateBankAccountSummary
    );

    bankAccountField.addEventListener(
        "change",
        updateBankAccountSummary
    );
}

  updateBankAccountSummary();
    const statusField = employeeForm.querySelector(
        '[name="employment_status"]'
    );

    const statusElement = card.querySelector(
        ".companyhr-summary-status"
    );

    if (statusElement) {
        statusElement.textContent = statusField
            ? statusField.selectedOptions[0]?.textContent.trim() || "وضعیت نامشخص"
            : "وضعیت نامشخص";

        statusElement.dataset.status = statusField?.value || "unknown";
    }

    const photoElement = card.querySelector(
        ".companyhr-summary-photo-img"
    );

    const photoPlaceholder = card.querySelector(
        ".companyhr-summary-photo-placeholder"
    );

    if (photoElement && photoPlaceholder && photoUrl) {
        photoElement.src = photoUrl;
        photoElement.hidden = false;
        photoPlaceholder.hidden = true;

        photoElement.onerror = function () {
            photoElement.hidden = true;
            photoPlaceholder.hidden = false;
        };
    }

    // شمارش نوع مدارک در پنل پیوست‌های فعلی
    const documentCards = Array.from(
        document.querySelectorAll(
            ".companyhr-identity-documents .companyhr-document-card"
        )
    );

    const missingCount = documentCards.filter(
        item => item.classList.contains("is-missing")
    ).length;

    const presentCount = documentCards.length - missingCount;

    setText(".summary-doc-present", toPersianDigits(presentCount));
    setText(".summary-doc-missing", toPersianDigits(missingCount));

    // کارت را پیش از تب‌ها، در همان والد مستقیم قرار بده
    const tabs = contentMain.querySelector(".companyhr-tabs");

    if (tabs && tabs.parentNode) {
        tabs.parentNode.insertBefore(card, tabs);
    } else {
        employeeForm.insertBefore(card, employeeForm.firstChild);
    }
}

// =========================================================
// پنل حرفه‌ای مدارک و پیوست‌های هویتی
// =========================================================

function buildIdentityDocumentsPanel() {

    const identityPanel = document.querySelector(
        '.companyhr-tab-panel[data-panel="identity"]'
    );

    if (!identityPanel) return;

    const docGroup = document.querySelector("#documents-group");

    if (!docGroup) return;


    // =====================================================
    // پاک کردن پنل قبلی
    // =====================================================

    const oldPanel = identityPanel.querySelector(
        ".companyhr-identity-documents"
    );

    if (oldPanel) {
        oldPanel.remove();
    }


    // =====================================================
    // حذف عنوان قدیمی «اسناد پیوست»
    // که توسط نسخه قبلی JavaScript ساخته شده بود
    // =====================================================

    docGroup.querySelectorAll(".doc-menu-header").forEach(function (element) {
        element.remove();
    });


    // =====================================================
    // انواع ثابت مدارک
    // =====================================================

    const fixedDocuments = [
        {
            value: "birth_certificate",
            title: "شناسنامه",
            icon: "📕"
        },
        {
            value: "national_card",
            title: "کارت ملی",
            icon: "🪪"
        },
        {
            value: "military_card",
            title: "کارت پایان خدمت",
            icon: "🎖️"
        },
        {
            value: "no_criminal_record",
            title: "گواهی سوءپیشینه",
            icon: "📄"
        },
        {
            value: "passport",
            title: "گذرنامه",
            icon: "🌐"
        }
    ];



// =====================================================
// تبدیل ردیف‌های واقعی به اطلاعات قابل استفاده

    // =====================================================
    // مقاطع تحصیلی
    // =====================================================

    const educationLevels = {
        diploma: "دیپلم",
        associate: "فوق دیپلم",
        bachelor: "کارشناسی",
        master: "کارشناسی ارشد",
        phd: "دکترا"
    };


// =====================================================
// پیدا کردن ردیف‌های واقعی اسناد
// =====================================================

const rows = Array.from(
    docGroup.querySelectorAll("tr.form-row")
);


// =====================================================
// تبدیل ردیف‌های واقعی به اطلاعات قابل استفاده
// =====================================================


function getDocumentInfo(row) {

    const typeSelect =
        row.querySelector('select[name$="-document_type"]');

    const educationSelect =
        row.querySelector('select[name$="-education_level"]');

    const fileLink =
        row.querySelector('td.field-file a[href]');

    const fileInput =
        row.querySelector(
            'input[type="file"][name$="-file"]'
        );

    // شناسه رکورد پیوست در پایگاه داده
    const idInput =
        row.querySelector('input[name$="-id"]');

    const documentId =
        idInput && idInput.value
            ? idInput.value
            : null;

    const documentType =
        typeSelect ? typeSelect.value : "";

    const educationLevel =
        educationSelect ? educationSelect.value : "";

    // تشخیص وضعیت حذف نرم از علامت نمایش‌داده‌شده توسط Django
    const deletedImage =
        row.querySelector('td.field-is_deleted img[alt]');

    const isDeleted =
        deletedImage
            ? deletedImage.alt.toLowerCase() === "true"
            : false;

    const hasNewFile =
        !!(
            fileInput &&
            fileInput.files &&
            fileInput.files.length > 0
        );

    // پیوست حذف‌شده نباید به‌عنوان مدرک فعال شناخته شود
    const hasFile =
        !isDeleted && (!!fileLink || hasNewFile);

    return {
        row: row,
        documentId: documentId,
        documentType: documentType,
        educationLevel: educationLevel,
        fileLink: fileLink,
        hasFile: hasFile,
        isDeleted: isDeleted
    };
}



// =====================================================
// اطلاعات تمام مدارک
// =====================================================

const documents =
    rows.map(function (row) {
        return getDocumentInfo(row);
    });


// =====================================================
// ساخت پنل و محل قرارگیری کارت‌ها
// =====================================================

const panel =
    document.createElement("div");

panel.className =
    "companyhr-identity-documents";


const panelTitle =
    document.createElement("div");

panelTitle.className =
    "documents-panel-title";

panelTitle.textContent =
    "اسناد و پیوست‌های هویتی";


const panelBody =
    document.createElement("div");

panelBody.className =
    "documents-panel-body";


const cardsContainer =
    document.createElement("div");
// =====================================================
// انتقال عکس پرسنلی به اولین کارت اسناد
// =====================================================

const photoRow = identityPanel.querySelector(
    ".form-row.field-photo"
);

if (photoRow) {

    const photoCard = document.createElement("div");

    photoCard.className =
        "companyhr-document-card companyhr-photo-document-card";

    const photoTitle = document.createElement("div");

    photoTitle.className =
        "companyhr-document-title";

    photoTitle.textContent = "عکس پرسنلی";

    photoCard.appendChild(photoTitle);

    photoCard.appendChild(photoRow);

    cardsContainer.appendChild(photoCard);
}

cardsContainer.className =
    "companyhr-document-cards";


panelBody.appendChild(
    cardsContainer
);

panel.appendChild(
    panelTitle
);

panel.appendChild(
    panelBody
);

function editDocument(documentInfo) {

    const row = documentInfo.row;

    if (!row) {
        return;
    }

    // -----------------------------------------
    // ساخت پنجره ویرایش
    // -----------------------------------------

    const oldModal = document.querySelector(
        ".companyhr-document-modal"
    );

    if (oldModal) {
        oldModal.remove();
    }

    const modal = document.createElement("div");
    modal.className = "companyhr-document-modal";

    const modalBox = document.createElement("div");
    modalBox.className = "companyhr-document-modal-box";

    // عنوان سند
    const typeSelect =
        row.querySelector('select[name$="-document_type"]');

    const educationSelect =
        row.querySelector('select[name$="-education_level"]');

    const titleInput =
        row.querySelector('input[name$="-title"]');

    const fileInput =
        row.querySelector('input[type="file"]');

    const issueDateInput =
        row.querySelector('input[name$="-issue_date"]');

    const descriptionInput =
        row.querySelector('textarea[name$="-description"]');

    let documentTitle = "ویرایش پیوست";

    if (typeSelect && typeSelect.value) {

        const selectedOption =
            typeSelect.options[
                typeSelect.selectedIndex
            ];

        if (selectedOption) {
            documentTitle =
                "ویرایش پیوست — " +
                selectedOption.textContent;
        }
    }

    if (
        typeSelect &&
        typeSelect.value === "education" &&
        educationSelect &&
        educationSelect.value
    ) {

        const selectedEducation =
            educationSelect.options[
                educationSelect.selectedIndex
            ];

        if (selectedEducation) {
            documentTitle =
                "ویرایش پیوست — مدرک تحصیلی — " +
                selectedEducation.textContent;
        }
    }

    // -----------------------------------------
    // سربرگ پنجره
    // -----------------------------------------

    const header = document.createElement("div");
    header.className =
        "companyhr-document-modal-header";

    const headerTitle = document.createElement("div");
    headerTitle.className =
        "companyhr-document-modal-title";

    headerTitle.textContent = documentTitle;

    const closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.className =
        "companyhr-document-modal-close";

    closeButton.textContent = "×";

    header.appendChild(headerTitle);
    header.appendChild(closeButton);

    // -----------------------------------------
    // بدنه پنجره
    // -----------------------------------------

    const body = document.createElement("div");
    body.className =
        "companyhr-document-modal-body";

    // عنوان
    if (titleInput) {

        const titleGroup =
            document.createElement("div");

        titleGroup.className =
            "companyhr-document-modal-field";

        const titleLabel =
            document.createElement("label");

        titleLabel.textContent =
            "عنوان / توضیح کوتاه";

        const newTitle =
            document.createElement("input");

        newTitle.type = "text";
        newTitle.className =
            "companyhr-document-modal-input";

        newTitle.value =
            titleInput.value || "";

        titleGroup.appendChild(titleLabel);
        titleGroup.appendChild(newTitle);

        body.appendChild(titleGroup);

        newTitle.dataset.target = "title";
    }

    
       // -----------------------------------------
    // تاریخ ثبت
    // -----------------------------------------

    if (issueDateInput) {

        const dateGroup =
            document.createElement("div");

        dateGroup.className =
            "companyhr-document-modal-field";

        const dateLabel =
            document.createElement("label");

        dateLabel.textContent =
            "تاریخ ثبت";

        const newDate =
            document.createElement("input");

        newDate.type = "text";
        newDate.id =
          "document-modal-issue-date-jalali-" +
           Date.now();

        newDate.className =
            "companyhr-document-modal-input vDateField";

        newDate.setAttribute(
            "autocomplete",
            "off"
        );

        newDate.setAttribute(
            "data-jdp",
            ""
        );

        newDate.setAttribute(
            "placeholder",
            "مثلاً ۱۴۰۵/۰۱/۱۵"
        );

        /*
         * مقدار اصلی تاریخ میلادی Django
         */
        const hiddenDate =
            document.createElement("input");

        hiddenDate.type = "hidden";

        hiddenDate.className =
            "companyhr-document-modal-hidden-date";

        /*
         * برای جلوگیری از تکراری شدن ID،
         * یک ID اختصاصی برای همین پنجره می‌سازیم.
         */
        const hiddenDateId =
            "document-modal-issue-date-gregorian-" +
            Date.now();

        hiddenDate.id =
            hiddenDateId;

        hiddenDate.name =
            "document_modal_issue_date_gregorian";

        hiddenDate.value =
            issueDateInput.value || "";

        /*
         * اتصال تقویم جلالی به فیلد مخفی میلادی
         */
        newDate.setAttribute(
            "data-jdp-target-value-input",
            "#" + hiddenDateId
        );

        newDate.setAttribute(
            "data-jdp-target-value-type",
            "gregorian"
        );

        /*
         * اگر تاریخ قبلی وجود داشته باشد،
         * آن را به جلالی تبدیل می‌کنیم.
         */
        if (hiddenDate.value) {

            const jalaliValue =
                gregorianToJalali(
                    hiddenDate.value
                );

            if (jalaliValue) {
                newDate.value =
                    jalaliValue;
            }
        }

        dateGroup.appendChild(
            dateLabel
        );

        dateGroup.appendChild(
            newDate
        );

        dateGroup.appendChild(
            hiddenDate
        );

        body.appendChild(
            dateGroup
        );

        /*
         * تقویم را مستقیماً با کلیک روی
         * فیلد باز می‌کنیم.
         */
        newDate.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                if (
                    typeof jalaliDatepicker !==
                    "undefined"
                ) {

                    jalaliDatepicker.show(
                        newDate
                    );

                }

            }
        );

       /*
 * بعد از قرار گرفتن input داخل DOM،
 * JalaliDatepicker را روی همین فیلد فعال می‌کنیم.
 */
    setTimeout(
      function () {

        if (
            typeof jalaliDatepicker !== "undefined" &&
            typeof jalaliDatepicker.startWatch === "function"
        ) {

            jalaliDatepicker.startWatch({
                selector: "#" + newDate.id,
                targetValueInput: "attr",
                targetValueType: "attr",
                persianDigits: true
            });

        }

     },
     100
 );

        /*
         * این ویژگی برای انتقال مقدار
         * هنگام ذخیره Modal استفاده می‌شود.
         */
        newDate.dataset.target =
            "issue_date";

        /*
         * وقتی تاریخ جلالی انتخاب شد،
         * مقدار میلادی در hiddenDate قرار می‌گیرد.
         *
         * در زمان ذخیره، همین مقدار را به
         * فیلد اصلی Django منتقل می‌کنیم.
         */
        newDate.addEventListener(
            "change",
            function () {

                if (
                    hiddenDate.value
                ) {

                    issueDateInput.value =
                        hiddenDate.value;

                }

            }
        );

    }
    // فایل فعلی
    const currentFile =
        row.querySelector(
            'td.field-file a[href]'
        );

    if (currentFile) {

        const fileGroup =
            document.createElement("div");

        fileGroup.className =
            "companyhr-document-modal-field";

        const fileLabel =
            document.createElement("label");

        fileLabel.textContent =
            "فایل فعلی";

        const viewLink =
            document.createElement("a");

        viewLink.href =
            currentFile.getAttribute("href");

        viewLink.target =
            "_blank";

        viewLink.rel =
            "noopener noreferrer";

        viewLink.className =
            "companyhr-document-modal-view";

        viewLink.textContent =
            "👁 مشاهده فایل";

        fileGroup.appendChild(fileLabel);
        fileGroup.appendChild(viewLink);

        body.appendChild(fileGroup);
    }

    // فایل جدید
   
    // فایل جدید
    if (fileInput) {

        const fileGroup = document.createElement("div");
        fileGroup.className = "companyhr-document-modal-field";

        const fileLabel = document.createElement("label");
        fileLabel.textContent = "فایل جدید";

        const newFile = document.createElement("input");
        newFile.type = "file";
        newFile.className = "companyhr-document-modal-file";

        // فعلاً پسوندهای مجاز فعلی را حفظ می‌کنیم.
        newFile.accept =
            ".pdf,.jpg,.jpeg,.png,.gif,.webp,.bmp,.tif,.tiff,.svg";

        fileGroup.appendChild(fileLabel);
        fileGroup.appendChild(newFile);
        body.appendChild(fileGroup);

        newFile.addEventListener("change", function () {

            if (!newFile.files || newFile.files.length === 0) {
                return;
            }

            if (!fileInput || !fileInput.isConnected) {
                console.error(
                    "ورودی اصلی فایل وجود ندارد یا از صفحه جدا شده است."
                );
                alert("ورودی فایل این مدرک پیدا نشد. صفحه را تازه‌سازی کنید.");
                return;
            }

            try {
                const selectedFile = newFile.files[0];
                const dataTransfer = new DataTransfer();

                dataTransfer.items.add(selectedFile);
                fileInput.files = dataTransfer.files;

                console.log("نام ورودی اصلی:", fileInput.name);
                console.log("فایل انتخاب‌شده:", selectedFile.name);
                console.log("تعداد فایل منتقل‌شده:", fileInput.files.length);
                console.log(
                    "نام فایل منتقل‌شده:",
                    fileInput.files[0]?.name || "انتقال انجام نشد"
                );

                if (
                    fileInput.files.length === 0 ||
                    fileInput.files[0].name !== selectedFile.name
                ) {
                    console.error("انتقال فایل به ورودی اصلی تأیید نشد.");
                    alert("انتقال فایل به فرم اصلی تأیید نشد.");
                }

            } catch (error) {
                console.error("خطا در انتقال فایل:", error);
                alert("انتقال فایل به فرم انجام نشد.");
            }
        });
    }


    // توضیحات
    if (descriptionInput) {

        const descriptionGroup =
            document.createElement("div");

        descriptionGroup.className =
            "companyhr-document-modal-field";

        const descriptionLabel =
            document.createElement("label");

        descriptionLabel.textContent =
            "توضیحات";

        const newDescription =
            document.createElement("textarea");

        newDescription.className =
            "companyhr-document-modal-textarea";

        newDescription.rows = 4;

        newDescription.value =
            descriptionInput.value || "";

        descriptionGroup.appendChild(
            descriptionLabel
        );

        descriptionGroup.appendChild(
            newDescription
        );

        body.appendChild(
            descriptionGroup
        );

        newDescription.dataset.target =
            "description";
    }

    // -----------------------------------------
    // دکمه‌های پایین پنجره
    // -----------------------------------------

    const footer =
        document.createElement("div");

    footer.className =
        "companyhr-document-modal-footer";

    const cancelButton =
        document.createElement("button");

    cancelButton.type = "button";

    cancelButton.className =
        "companyhr-document-modal-cancel";

    cancelButton.textContent =
        "انصراف";

    const saveButton =
        document.createElement("button");

    saveButton.type = "button";

    saveButton.className =
        "companyhr-document-modal-save";

    saveButton.textContent =
        "💾 ذخیره";

    footer.appendChild(cancelButton);
    footer.appendChild(saveButton);

    // -----------------------------------------
    // مونتاژ پنجره
    // -----------------------------------------

    modalBox.appendChild(header);
    modalBox.appendChild(body);
    modalBox.appendChild(footer);

    modal.appendChild(modalBox);

    document.body.appendChild(modal);

    // -----------------------------------------
    // بستن پنجره
    // -----------------------------------------

    function closeModal() {
        modal.remove();
    }

    closeButton.addEventListener(
        "click",
        closeModal
    );

    cancelButton.addEventListener(
        "click",
        closeModal
    );

    modal.addEventListener(
        "click",
        function (event) {

            if (event.target === modal) {
                closeModal();
            }
        }
    );

    // -----------------------------------------
    // فعلاً ذخیره واقعی انجام نمی‌شود
    // -----------------------------------------
    saveButton.addEventListener(
        "click",
        function () {

            // -----------------------------------------
            // انتقال عنوان
            // -----------------------------------------

            if (titleInput) {

                const newTitle =
                    body.querySelector(
                        '[data-target="title"]'
                    );

                if (newTitle) {
                    titleInput.value =
                        newTitle.value;
                }
            }

            // -----------------------------------------
            // انتقال تاریخ صدور
            // -----------------------------------------

            if (issueDateInput) {

                const newDate =
                    body.querySelector(
                        '[data-target="issue_date"]'
                    );

                const hiddenDate =
                    body.querySelector(
                        ".companyhr-document-modal-hidden-date"
                    );

                if (hiddenDate && hiddenDate.value) {

                    issueDateInput.value =
                        hiddenDate.value;

                } else if (newDate && newDate.value) {

                    issueDateInput.value =
                        newDate.value;

                }
            }

            // -----------------------------------------
            // انتقال توضیحات
            // -----------------------------------------

            if (descriptionInput) {

                const newDescription =
                    body.querySelector(
                        '[data-target="description"]'
                    );

                if (newDescription) {
                    descriptionInput.value =
                        newDescription.value;
                }
            }

            // -----------------------------------------
            // انتقال فایل
            // -----------------------------------------

            const modalFile =
                body.querySelector(
                    ".companyhr-document-modal-file"
                );

            // -----------------------------------------
            // انتقال فایل انتخاب‌شده به فرم اصلی Django
            // -----------------------------------------

            if (
                   modalFile &&
                   modalFile.files &&
                   modalFile.files.length > 0 &&
                   fileInput
            ) {

                 const selectedFile =
                        modalFile.files[0];

                try {

                 const dataTransfer = new DataTransfer();

                dataTransfer.items.add(selectedFile);

                fileInput.files = dataTransfer.files;

                console.log("ورودی فایل:", fileInput);
                console.log(
                     "تعداد فایل پس از انتقال:",
                      fileInput.files.length
                    );
                console.log(
                     "نام فایل پس از انتقال:",
                     fileInput.files.length > 0
                     ? fileInput.files[0].name
                     : "هیچ فایلی منتقل نشده است"
                    );


                } catch (error) {

                      console.error(
                           "خطا در انتقال فایل:",
                             error
                         );

                        alert(
                                  "انتقال فایل به فرم انجام نشد."
                              );

                         return;
                     }
                }

            // -----------------------------------------
            // بستن پنجره
            // -----------------------------------------

            closeModal();

            // -----------------------------------------
            // مشخص کردن ردیف ویرایش‌شده
            // -----------------------------------------

            row.classList.add(
                "companyhr-document-editing"
            );

            // -----------------------------------------
            // اطلاع به کاربر
            // -----------------------------------------

            const message =
                document.createElement("div");

            message.className =
                "companyhr-document-save-message";

            message.textContent =
                "تغییرات در فرم ثبت شد. برای ذخیره نهایی، دکمه «ذخیره» پایین صفحه را بزنید.";

            document.body.appendChild(message);

            setTimeout(function () {

                message.remove();

            }, 4000);
            // -----------------------------------------
            // به‌روزرسانی کارت‌های اسناد
            // -----------------------------------------

           setTimeout(function () {

                 buildIdentityDocumentsPanel();

            }, 50);
        }
    );

}
    // =====================================================
    // ساخت کارت یک نوع سند
    // =====================================================

    function createDocumentCard(
        titleText,
        icon,
        matchingDocuments,
        forceShow
    ) {


        // -----------------------------------------------
        // آیا حداقل یک فایل وجود دارد؟
        // -----------------------------------------------

        const documentsWithFile =
            matchingDocuments.filter(function (doc) {

                return doc.hasFile;

            });


        const hasFile =
            documentsWithFile.length > 0;


        // -----------------------------------------------
        // اگر نباید نمایش داده شود
        // -----------------------------------------------

        if (!forceShow && !hasFile) {
            return null;
        }


        // -----------------------------------------------
        // کارت
        // -----------------------------------------------

        const card =
            document.createElement("div");

        card.className =
            "companyhr-document-card";


        if (!hasFile) {

            card.classList.add(
                "is-missing"
            );

        }


        // =================================================
        // آیکون
        // =================================================

        const iconElement =
            document.createElement("div");

        iconElement.className =
            "companyhr-document-icon";

        iconElement.textContent =
            icon;


        // =================================================
        // اطلاعات
        // =================================================

        const info =
            document.createElement("div");

        info.className =
            "companyhr-document-info";


        // -------------------------------------------------
        // عنوان
        // -------------------------------------------------

        const cardTitle =
            document.createElement("div");

        cardTitle.className =
            "companyhr-document-title";

        cardTitle.textContent =
            titleText;

        info.appendChild(cardTitle);


        // -------------------------------------------------
        // وضعیت
        // -------------------------------------------------

        const status =
            document.createElement("div");

        status.className =
            "companyhr-document-status";


        if (hasFile) {

            status.textContent =
                documentsWithFile.length + " فایل";

        } else {

            status.textContent =
                "مدرکی ثبت نشده است";
        }


        info.appendChild(status);

        // -------------------------------------------------
// تاریخ ثبت
// -------------------------------------------------

        const documentDates =
    matchingDocuments
        .map(function (documentInfo) {

            if (!documentInfo.row) {
                return "";
            }

            const issueDateInput =
                documentInfo.row.querySelector(
                    'input[name$="-issue_date"]'
                );

            return issueDateInput
                ? issueDateInput.value
                : "";

        })
        .filter(function (dateValue) {
            return dateValue;
        });


        const documentDate =
            document.createElement("div");

        documentDate.className =
            "companyhr-document-date";


    if (documentDates.length > 0) {

             /*
     * آخرین تاریخ ثبت‌شده
     */
      const latestDate =
        documentDates[documentDates.length - 1];

      const jalaliDate =
        gregorianToJalali(latestDate);

       documentDate.textContent =
            "تاریخ ثبت: " +
             (jalaliDate || latestDate);

    } else {

         documentDate.textContent =
            "تاریخ ثبت: ثبت نشده";

    }


    info.appendChild(
         documentDate
        );


        // =================================================
        // دکمه‌های عملیات
        // =================================================

        const actions =
            document.createElement("div");

        actions.className =
            "companyhr-document-actions";


        // -------------------------------------------------
        // برای هر فایل
        // -------------------------------------------------

        documentsWithFile.forEach(function (
            documentInfo,
            index
        ) {


            // =============================================
            // دکمه مشاهده
            // =============================================

            if (
                documentInfo.fileLink &&
                documentInfo.fileLink.getAttribute("href")
            ) {

                const viewLink =
                    document.createElement("a");

                viewLink.className =
                    "companyhr-document-view";

                viewLink.href =
                    documentInfo.fileLink.getAttribute(
                        "href"
                    );

                viewLink.target =
                    "_blank";

                viewLink.rel =
                    "noopener noreferrer";


                if (
                    documentsWithFile.length > 1
                ) {

                    viewLink.textContent =
                        "👁 مشاهده " + (index + 1);

                } else {

                    viewLink.textContent =
                        "👁 مشاهده";
                }


                actions.appendChild(
                    viewLink
                );
            }


            // =============================================
            // دکمه ویرایش
            // =============================================

            const editButton =
                document.createElement("button");

            editButton.type = "button";
            editButton.className =
                "companyhr-document-edit";

            editButton.textContent = "✏️ ویرایش";

            editButton.addEventListener(
                "click",
                function (event) {
                    event.preventDefault();
                    event.stopPropagation();

                    editDocument(documentInfo);
                }
            );

            actions.appendChild(editButton);

            // =============================================
            // دکمه حذف نرم پیوست
            // =============================================

            if (documentInfo.documentId) {

                const deleteButton =
                    document.createElement("button");

                deleteButton.type = "button";
                deleteButton.className =
                    "companyhr-document-delete";

                deleteButton.textContent = "🗑️ حذف پیوست";

                deleteButton.addEventListener(
                    "click",
                    function (event) {
                        event.preventDefault();
                        event.stopPropagation();

                        if (!window.confirm(
                            "آیا از حذف این پیوست مطمئن هستید؟\n\n" +
                            "فایل اصلی از سرور پاک نمی‌شود."
                        )) {
                            return;
                        }

                        const csrfInput =
                            document.querySelector(
                                'input[name="csrfmiddlewaretoken"]'
                            );

                        const csrfToken =
                            csrfInput ? csrfInput.value : "";

                        if (!csrfToken) {
                            alert(
                                "توکن امنیتی پیدا نشد. صفحه را تازه‌سازی کنید."
                            );
                            return;
                        }

                        deleteButton.disabled = true;
                        deleteButton.textContent = "در حال حذف...";

                        fetch(
                            "/personnel/documents/" +
                            encodeURIComponent(documentInfo.documentId) +
                            "/soft-delete/",
                            {
                                method: "POST",
                                credentials: "same-origin",
                                headers: {
                                    "X-CSRFToken": csrfToken,
                                    "X-Requested-With": "XMLHttpRequest",
                                    "Accept": "application/json"
                                }
                            }
                        )
                        .then(function (response) {
                            return response.json().then(function (data) {
                                if (!response.ok || !data.success) {
                                    throw new Error(
                                        data.message || "حذف پیوست انجام نشد."
                                    );
                                }
                                return data;
                            });
                        })
                        .then(function () {
                            alert("پیوست با موفقیت به‌صورت نرم حذف شد.");
                            window.location.reload();
                        })
                        .catch(function (error) {
                            console.error("خطا در حذف پیوست:", error);

                            alert(
                                error.message ||
                                "ارتباط با سرور برقرار نشد."
                            );

                            deleteButton.disabled = false;
                            deleteButton.textContent = "🗑️ حذف پیوست";
                        });
                    }
                );

                actions.appendChild(deleteButton);
            }

        });

        // =================================================
        // اگر مدرک موجود نیست
        // =================================================
if (!hasFile) {
    const missingText = document.createElement("div");
    missingText.className = "companyhr-document-missing";
    missingText.textContent = "مدرکی ثبت نشده است";
    info.appendChild(missingText);

    const editButton = document.createElement("button");
    editButton.type = "button";
    editButton.className = "companyhr-document-edit";
    editButton.textContent = "✏️ ویرایش";

    editButton.addEventListener(
        "click",
        function (event) {
            event.preventDefault();
            event.stopPropagation();

            /*
             * اگر برای این نوع سند، ردیفی از قبل وجود داشته باشد،
             * همان ردیف را برای ویرایش باز می‌کنیم.
             */
            if (matchingDocuments.length > 0) {
                editDocument(
                    matchingDocuments[0]
                );
                return;
            }

            /*
             * اگر هنوز هیچ ردیفی برای این سند وجود ندارد،
             * از مکانیزم استاندارد Django Admin برای
             * اضافه کردن ردیف جدید استفاده می‌کنیم.
             */

            const addRowLink =
                docGroup.querySelector(".add-row a");

            if (!addRowLink) {
                alert(
                    "دکمه افزودن پیوست پیدا نشد."
                );
                return;
            }

            const totalForms =
                docGroup.querySelector(
                    'input[name$="-TOTAL_FORMS"]'
                );

            if (!totalForms) {
                alert(
                    "فرم ثبت پیوست پیدا نشد."
                );
                return;
            }

            /*
             * شماره ردیف جدید را قبل از کلیک روی
             * دکمه افزودن ذخیره می‌کنیم.
             */
            const formIndex =
                parseInt(
                    totalForms.value,
                    10
                );

            /*
             * اجازه می‌دهیم خود Django Admin
             * ردیف جدید را بسازد.
             */
            addRowLink.click();

            /*
             * کمی صبر می‌کنیم تا Django ردیف جدید
             * را کامل به جدول اضافه کند.
             */
            setTimeout(function () {

                const newTypeSelect =
                    docGroup.querySelector(
                        'select[name$="-' +
                        formIndex +
                        '-document_type"]'
                    );

                let newRow = null;

                if (newTypeSelect) {
                    newRow =
                        newTypeSelect.closest(
                            "tr.form-row"
                        );
                }

                if (!newRow) {
                    alert(
                        "ردیف جدید پیوست ساخته نشد."
                    );
                    return;
                }

                /*
                 * نوع سند را مطابق کارتی که روی آن
                 * کلیک شده انتخاب می‌کنیم.
                 */
                const newDocumentType =
                    newRow.querySelector(
                        'select[name$="-document_type"]'
                    );

                if (
                    newDocumentType &&
                    card.dataset.documentType
                ) {
                    newDocumentType.value =
                        card.dataset.documentType;
                }

                /*
                 * اگر سند مربوط به مدرک تحصیلی باشد،
                 * سطح تحصیلی را نیز تنظیم می‌کنیم.
                 */
                const newEducationLevel =
                    newRow.querySelector(
                        'select[name$="-education_level"]'
                    );

                if (
                    newEducationLevel &&
                    card.dataset.educationLevel
                ) {
                    newEducationLevel.value =
                        card.dataset.educationLevel;
                }

                /*
                 * وضعیت نمایش فیلدهای ردیف جدید
                 * را دوباره به‌روزرسانی می‌کنیم.
                 */
                updateAllDocumentRows();

                /*
                 * اطلاعات ردیف جدید را می‌گیریم
                 * و پنجره ویرایش را باز می‌کنیم.
                 */
                const newDocumentInfo =
                    getDocumentInfo(newRow);

                editDocument(
                    newDocumentInfo
                );

            }, 50);
        }
    );

    actions.appendChild(
        editButton
    );
}

        // =================================================
        // ساخت کارت
        // =================================================

        card.appendChild(
            iconElement
        );

        card.appendChild(
            info
        );


        if (actions.children.length > 0) {

            card.appendChild(
                actions
            );
        }


        return card;
    }


    // =================================================

    // کلیک روی کارت برای مشاهده اولین فایل

    // =================================================


    // =====================================================
    // مدارک ثابت
    // =====================================================

    fixedDocuments.forEach(function (documentType) {

    const matchingDocuments =
        documents.filter(function (doc) {

            return (
                doc.documentType ===
                documentType.value
            );

        });

    const card =
        createDocumentCard(
            documentType.title,
            documentType.icon,
            matchingDocuments,
            true
        );

    if (card) {

        card.dataset.documentType =
            documentType.value;

        cardsContainer.appendChild(
            card
        );
    }

});


    // =====================================================
    // مدارک تحصیلی
    // فقط مقاطعی که فایل دارند
    // =====================================================

    Object.keys(educationLevels).forEach(function (level) {


        const matchingDocuments =
            documents.filter(function (doc) {

                return (
                    doc.documentType ===
                        "education" &&

                    doc.educationLevel ===
                        level &&

                    doc.hasFile
                );

            });


        if (!matchingDocuments.length) {
            return;
        }


        const card =
            createDocumentCard(
                "مدرک تحصیلی — " +
                    educationLevels[level],

                "🎓",

                matchingDocuments,

                false
            );


        if (card) {

            cardsContainer.appendChild(
                card
            );
        }

    });


    // =====================================================
    // سایر
    // فقط در صورت وجود فایل
    // =====================================================

   // =====================================================
// سایر مستندات
// =====================================================

    const otherDocuments =
        documents.filter(function (doc) {

            return (
                doc.documentType === "other"
            );

        });

    const otherCard =
        createDocumentCard(
            "سایر مستندات",
            "📁",
            otherDocuments,
            true
        );

    if (otherCard) {

        otherCard.dataset.documentType = "other";

        cardsContainer.appendChild(
            otherCard
        );
    }


    // =====================================================
    // اضافه کردن کارت‌ها به پنل
    // =====================================================

    panel.appendChild(
        cardsContainer
    );


// =====================================================
// قرار دادن پنل مدارک
// =====================================================

docGroup.parentNode.insertBefore(
    panel,
    docGroup
);

// =====================================================
// مخفی کردن لیست قدیمی اسناد
// =====================================================

docGroup.style.display = "none";
buildEmployeeSummaryCard();
}

// =========================================================
// اجرای نهایی
// =========================================================

buildEmployeeTabs();
setupIdentityBehavior();
setupEmploymentBehavior();
setupFamilyCollapse();
setupDeleteWarning();
setupUnsavedWarning();

// فعلاً این دو تابع عمداً اجرا نمی‌شوند
// setupDocumentHyperlinkMenu();
// setupAllInlinesViewEditMode();

setTimeout(function () {

    updateAllDocumentRows();

    // ساخت پنل مدارک فقط یک بار
    buildIdentityDocumentsPanel();

    if (familyGroup) {
        familyGroup
            .querySelectorAll(".inline-related")
            .forEach(function (row) {
                prepareFamilyDates(row);
            });
    }

}, 300);

});