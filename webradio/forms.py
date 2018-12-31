from django import forms
from webradio.models import Stream, Station


class StationForm(forms.ModelForm):
    default_stream = forms.ModelChoiceField(
        queryset=Stream.objects.none(), required=False)

    class Meta:
        model = Station
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StationForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['default_stream'].queryset = Stream.objects.filter(
                station=self.instance)
            self.fields['default_stream'].required = True
            default_stream = self.instance.get_default_stream()
            if default_stream:
                self.fields['default_stream'].initial = default_stream.id

    def save(self, *args, **kwargs):
        if self.instance.pk:
            stream = self.cleaned_data['default_stream']
            stream.default = True
            stream.save()
        return super(StationForm, self).save(*args, **kwargs)
