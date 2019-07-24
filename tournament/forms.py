# -*- coding: utf-8 -*-
from django import forms


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    email = forms.EmailField(label='Email (@appliedtech.ru)')

    first_name.widget.attrs.update({'class': 'form-control'})
    last_name.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})


class ResultForm(forms.Form):
    set1res1 = forms.CharField(label='Результат участника #1 в 1-м сете', max_length=2)
    set1res2 = forms.CharField(label='Результат участника #2 в 1-м сете', max_length=2)
    set2res1 = forms.CharField(label='Результат участника #1 во 2-м сете', max_length=2)
    set2res2 = forms.CharField(label='Результат участника #2 во 2-м сете', max_length=2)
    set3res1 = forms.CharField(label='Результат участника #1 в 3-м сете', max_length=2)
    set3res2 = forms.CharField(label='Результат участника #2 в 3-м сете', max_length=2)
    set4res1 = forms.CharField(label='Результат участника #1 в 4-м сете', max_length=2)
    set4res2 = forms.CharField(label='Результат участника #2 в 4-м сете', max_length=2)
    set5res1 = forms.CharField(label='Результат участника #1 в 5-м сете', max_length=2)
    set5res2 = forms.CharField(label='Результат участника #2 в 5-м сете', max_length=2)

    set1res1.widget.attrs.update({'style': 'max-width: 25px'})
    set1res2.widget.attrs.update({'style': 'max-width: 25px'})
    set2res1.widget.attrs.update({'style': 'max-width: 25px'})
    set2res2.widget.attrs.update({'style': 'max-width: 25px'})
    set3res1.widget.attrs.update({'style': 'max-width: 25px'})
    set3res2.widget.attrs.update({'style': 'max-width: 25px'})
    set4res1.widget.attrs.update({'style': 'max-width: 25px'})
    set4res2.widget.attrs.update({'style': 'max-width: 25px'})
    set5res1.widget.attrs.update({'style': 'max-width: 25px'})
    set5res2.widget.attrs.update({'style': 'max-width: 25px'})
