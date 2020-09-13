from django import forms

class SearchMoviesForm(forms.Form):
    title = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Movie title', 'label': ''})
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].label = ''

