from django import forms


class PersianDateInput(forms.DateInput):
    input_type = "text"

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "format",
            "%Y-%m-%d",
        )

        super().__init__(*args, **kwargs)

        self.attrs.update({
            "class": "vDateField",
            "autocomplete": "off",
            "placeholder": "مثلاً 1405/01/15",
            "data-jdp": "",
        })