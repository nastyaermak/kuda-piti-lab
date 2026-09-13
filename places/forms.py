from django import forms


class PlaceForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        strip=True,
        label='Назва',
    )
    place_type = forms.CharField(
        max_length=50,
        strip=True,
        label='Тип місця',
        help_text='Наприклад: кафе, парк, бар.',
    )
    location = forms.CharField(
        max_length=150,
        strip=True,
        required=False,
        label='Локація',
        help_text='Залиште порожнім, якщо хочете зберегти це в секреті.',
    )
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        label='Рейтинг',
        help_text='Ціле число від 1 до 5.',
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Опис',
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.strip():
            raise forms.ValidationError('Назва не може бути порожньою.')
        return name
