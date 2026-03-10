from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Company, EmployeeProfile

INDIAN_STATES = [
    ('', 'Select State'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Ladakh', 'Ladakh'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Odisha', 'Odisha'),
    ('Puducherry', 'Puducherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),
    ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'),
]

class CompanySignupForm(forms.ModelForm):
    full_name = forms.CharField(max_length=255, label="Full Name (Owner/Admin)", required=True)
    email = forms.EmailField(label="Work Email", required=True)
    phone = forms.CharField(max_length=15, label="Mobile Number", required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    state = forms.ChoiceField(choices=INDIAN_STATES, required=True)

    class Meta:
        model = Company
        fields = ['name', 'logo', 'country', 'state', 'city', 'size', 'industry', 'primary_use', 'no_of_branches', 'gstin', 'referral_source']
        labels = {
            'name': 'Company / Business Name',
            'logo': 'Company Logo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure model-based fields that should be mandatory are explicitly required
        self.fields['name'].required = True
        self.fields['country'].required = True
        self.fields['city'].required = True
        # Optional fields based on model but could be made mandatory here if needed
        # self.fields['size'].required = True 
        # self.fields['industry'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class AdminEmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to use default or OTP link")
    designation = forms.CharField(max_length=100, required=False)
    department = forms.CharField(max_length=100, required=False)
    branch = forms.CharField(max_length=100, required=False)
    shift = forms.CharField(max_length=100, required=False)

    class Meta:
        model = EmployeeProfile
        fields = ['employee_code', 'joining_date', 'role']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        self._company = company
        super().__init__(*args, **kwargs)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class EmployeeLoginForm(forms.Form):
    employee_id = forms.CharField(label="Employee ID", max_length=50)
    phone = forms.CharField(label="Mobile Number", max_length=15)
