from django import forms

from email_list.models import Client, MailingMessage, MailingSettings, Attempt

word_blacklist = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)

    def clean_description(self):
        cleaned_data = self.cleaned_data["description"]

        for word in word_blacklist:
            if word in cleaned_data.lower():
                raise forms.ValidationError(
                    f"Вы используете запрещенное слово '{word}' в описании клиента"
                )

        return cleaned_data


class MailingMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        exclude = ("owner",)

    def clean_subject(self):
        cleaned_data = self.cleaned_data["subject"]

        for word in word_blacklist:
            if word in cleaned_data.lower():
                raise forms.ValidationError(
                    f"Вы используете запрещенное слово '{word}' в теме письма"
                )

        return cleaned_data

    def clean_message(self):
        cleaned_data = self.cleaned_data["message"]

        for word in word_blacklist:
            if word in cleaned_data.lower():
                raise forms.ValidationError(
                    f"Вы используете запрещенное слово '{word}' в сообщении"
                )

        return cleaned_data


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        exclude = ("owner", "status", "is_active")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["mail_message"].queryset = MailingMessage.objects.filter(owner=user)
        self.fields["clients"].queryset = Client.objects.filter(owner=user)


class MailingSettingsModeratorsForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = ("is_active",)


class AttemptForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Attempt
        fields = "__all__"
