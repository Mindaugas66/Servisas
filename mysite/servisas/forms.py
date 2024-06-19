from .models import OrderComment, Order
from django import forms
from .models import Profile
from django import forms
from django.contrib.auth.models import User


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = OrderComment
        fields = ["comment"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class MyDateInput(forms.DateInput):
    input_type = 'date'


class UserOrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["car", "deadline"]
        widgets = {"deadline": MyDateInput}
