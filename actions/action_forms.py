from django import forms

VAMPIRE_OPTIONS = (
    ('p', 'Turn off power strip',),
    ('u', 'Unplug the device',),
    ('s', 'Use a smart power strip',),
    ('k', 'Skip',),
)

class VampireSlayerWidget(forms.RadioSelect):
    def __init__(self, *args, **kwargs):
        html_class = {"class": "vampire_slayer"}
        if "attrs" in kwargs:
            kwargs["attrs"].update(html_class)
        else:
            kwargs["attrs"] = html_class
        return super(VampireSlayerWidget, self).__init__(*args, **kwargs)

class VampirePowerWorksheetForm(forms.Form):
    television = forms.ChoiceField(required=False, choices=VAMPIRE_OPTIONS, widget=VampireSlayerWidget)
    dvd_player = forms.ChoiceField(required=False, choices=VAMPIRE_OPTIONS, widget=VampireSlayerWidget)
    cable_box = forms.ChoiceField(required=False, choices=VAMPIRE_OPTIONS, widget=VampireSlayerWidget)
    game_system = forms.ChoiceField(required=False, choices=VAMPIRE_OPTIONS, widget=VampireSlayerWidget)
    cell_phone = forms.ChoiceField(required=False, choices=VAMPIRE_OPTIONS, widget=VampireSlayerWidget)
    monitor = forms.ChoiceField(required=False, choices=VAMPIRE_OPTIONS, widget=VampireSlayerWidget)