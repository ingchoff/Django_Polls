from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.http import request

from polls.models import Poll


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('%(value)s ไม่ใช่เลขคู่', params={'value': value})


class PollForm(forms.Form):
    title = forms.CharField(max_length=100, label="ชื่อโพล", required=True)
    email = forms.CharField(validators=[validators.validate_email])
    no_questions = forms.IntegerField(label="จำนวนคำถาม", min_value=0, max_value=10, required=True, validators=[validate_even])
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def clean_title(self):
        data = self.cleaned_data['title']

        if "IT" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")

        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            self.add_error('end_date', 'โปรดเลือกวันที่สิ้นสุด')
            # raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')
        elif end and not start:
            self.add_error('start_date', 'โปรดเลือกวันที่เริ่มต้น')
            # raise forms.ValidationError('โปรดเลือกวันที่เริ่มต้น')


class CommentForm(forms.Form):
    title = forms.CharField(max_length=100, label='title', required=True)
    body = forms.CharField(widget=forms.Textarea, max_length=500, label='body', required=True)
    email = forms.CharField(validators=[validators.validate_email], required=False)
    tel = forms.CharField(max_length=10, label='tel', required=False)

    def clean_title(self):
        data = self.cleaned_data['title']

        if len(data) > 100:
            raise forms.ValidationError("title ต้องไม่เกิน 100 ตัวอักษร")

        return data

    def clean_body(self):
        data = self.cleaned_data['body']

        if len(data) > 500:
            raise forms.ValidationError("body ต้องไม่เกิน 500 ตัวอักษร")

        return data

    def clean_tel(self):
        data = self.cleaned_data['tel']

        if data.isalpha():
            raise forms.ValidationError("ต้องใส่เป็นตัวเลขเท่านั้น")

        elif len(data) != 10 and data != '':
            raise forms.ValidationError("ต้องกรอกครบ 10 หลัก")

        return data

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        tel = cleaned_data.get('tel')

        if email == '' and tel == '':
            raise forms.ValidationError('ต้องกรอก email หรือ tel.')


class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=100, label='Question Text:')
    choice_text = forms.CharField(max_length=100, label='Choice Text')
    choice_value = forms.IntegerField(min_value=0, max_value=5, label='Choice Value')


class MyLoginForm(forms.Form):
    user = forms.CharField(max_length=100, label='Username:')
    password = forms.CharField(widget=forms.PasswordInput, label='Password:')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('user')
        password = cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            raise forms.ValidationError('Wrong username or password!')


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100, label='Old Password:')
    new_password = forms.CharField(max_length=100, label='New Password:')
    confirm_password = forms.CharField(max_length=100, label='Confirm Password:', required=False)

    def clean_new_password(self):
        data = self.cleaned_data['new_password']

        if len(data) <= 8:
            raise forms.ValidationError("รหัสผ่านต้องมีมากกว่า 8 ตัวอักษร")
        return data

    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')

        if new != confirm:
            raise forms.ValidationError('รหัสผ่านใหม่ กับ confirm password ไม่ตรงกัน')


class PollModelForm(forms.ModelForm):
    email = forms.CharField(validators=[validators.validate_email])
    no_questions = forms.IntegerField(label="จำนวนคำถาม", min_value=0, max_value=10, required=True,
                                      validators=[validate_even])

    class Meta:
        model = Poll
        exclude = ['del_flag']

    def clean_title(self):
        data = self.cleaned_data['title']

        if "IT" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")

        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')

        if start and not end:
            self.add_error('end_date', 'โปรดเลือกวันที่สิ้นสุด')
            # raise forms.ValidationError('โปรดเลือกวันที่สิ้นสุด')
        elif end and not start:
            self.add_error('start_date', 'โปรดเลือกวันที่เริ่มต้น')
            # raise forms.ValidationError('โปรดเลือกวันที่เริ่มต้น')
