# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    email = forms.EmailField(label='Email (@appliedtech.ru)')

    first_name.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})


class ResultForm(forms.Form):
    set1res1 = forms.IntegerField(label='Результат участника #1 в 1-м сете', max_value=99, min_value=0)
    set1res2 = forms.IntegerField(label='Результат участника #2 в 1-м сете', max_value=99, min_value=0)
    set2res1 = forms.IntegerField(label='Результат участника #1 во 2-м сете', max_value=99, min_value=0)
    set2res2 = forms.IntegerField(label='Результат участника #2 во 2-м сете', max_value=99, min_value=0)
    set3res1 = forms.IntegerField(label='Результат участника #1 в 3-м сете', max_value=99, min_value=0)
    set3res2 = forms.IntegerField(label='Результат участника #2 в 3-м сете', max_value=99, min_value=0)
    set4res1 = forms.IntegerField(label='Результат участника #1 в 4-м сете', max_value=99, min_value=0)
    set4res2 = forms.IntegerField(label='Результат участника #2 в 4-м сете', max_value=99, min_value=0)
    set5res1 = forms.IntegerField(label='Результат участника #1 в 5-м сете', max_value=99, min_value=0)
    set5res2 = forms.IntegerField(label='Результат участника #2 в 5-м сете', max_value=99, min_value=0)

    set1res1.widget.attrs.update({'style': 'max-width: 40px'})
    set1res2.widget.attrs.update({'style': 'max-width: 40px'})
    set2res1.widget.attrs.update({'style': 'max-width: 40px'})
    set2res2.widget.attrs.update({'style': 'max-width: 40px'})
    set3res1.widget.attrs.update({'style': 'max-width: 40px'})
    set3res2.widget.attrs.update({'style': 'max-width: 40px'})
    set4res1.widget.attrs.update({'style': 'max-width: 40px'})
    set4res2.widget.attrs.update({'style': 'max-width: 40px'})
    set5res1.widget.attrs.update({'style': 'max-width: 40px'})
    set5res2.widget.attrs.update({'style': 'max-width: 40px'})

    def clean(self):
        cleaned_data = super().clean()

        for i in range(1, 6):
            f1 = "set{}res1".format(i)
            f2 = "set{}res2".format(i)
            r1 = cleaned_data.get(f1)
            r2 = cleaned_data.get(f2)

            if r1 > r2:
                if r1 - r2 > 2:
                    if r1 != 11:
                        self.add_error(f1, "Result must be 11")
                elif r1 - r2 == 1:
                    self.add_error(f1, "Point difference must be at least 2")
                else:
                    if r1 < 11:
                        self.add_error(f1, "Result must be at least 11")
            elif r2 > r1:
                if r2 - r1 > 2:
                    if r2 != 11:
                        self.add_error(f2, "Result must be 11")
                elif r2 - r1 == 1:
                    self.add_error(f2, "Point difference must be at least 2")
                else:
                    if r2 < 11:
                        self.add_error(f2, "Result must be at least 11")
            else:
                self.add_error(f1, ValidationError(_("Results cannot be equal")))
