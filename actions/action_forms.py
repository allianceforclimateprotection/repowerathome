from django import forms
from django.template.loader import render_to_string

VAMPIRE_OPTIONS = (
    ('p', 'Turn off power strip',),
    ('u', 'Unplug the device',),
    ('s', 'Use a smart power strip',),
    ('k', 'Skip',),
)

class VampireSlayerWidget(forms.RadioSelect):
    def __init__(self, attrs=None, recommended=None, *args, **kwargs):
        html_class = {"class": "vampire_slayer"}
        if attrs:
            attrs.update(html_class)
        else:
            attrs = html_class
        return super(VampireSlayerWidget, self).__init__(attrs=attrs, *args, **kwargs)

class VampireField(forms.ChoiceField):
    def __init__(self, recommended=None, choices=None, savings=0, widget=None, *args, **kwargs):
        if not choices:
            choices=VAMPIRE_OPTIONS
        self.savings = savings
        self.recommended = recommended
        if not widget:
            widget = VampireSlayerWidget
        return super(VampireField, self).__init__(choices=choices, widget=widget, *args, **kwargs)

class VampirePowerWorksheetForm(forms.Form):
    television = VampireField(savings=150, required=False, recommended='s')
    dvd_player = VampireField(savings=9, required=False, recommended='s', label="DVD Player")
    cable_box = VampireField(savings=13, required=False, recommended='s', label="Cable Box")
    game_system = VampireField(savings=30, required=False, recommended='s', label="Video Game System")
    cell_phone = VampireField(savings=4, required=False, recommended='u', label="Cell Phone")
    monitor = VampireField(savings=3, required=False, recommended='s')
    
    def ajax_data(self):
        return {"total_savings": self.total_savings()}
    
    def total_savings(self):
        total_savings = 0
        for bound_field in self:
            total_savings += bound_field.field.savings if bound_field.data in ['p', 'u', 's'] else 0
        return total_savings