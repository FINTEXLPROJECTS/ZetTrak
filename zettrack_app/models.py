from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class Company(models.Model):
    COMPANY_SIZE_CHOICES = [
        ('1-10', '1-10'),
        ('11-50', '11-50'),
        ('51-200', '51-200'),
        ('200+', '200+'),
    ]
    PRIMARY_USE_CHOICES = [
        ('attendance_only', 'Attendance only'),
        ('attendance_payroll', 'Attendance + Payroll'),
    ]
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=20, choices=COMPANY_SIZE_CHOICES, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    primary_use = models.CharField(max_length=50, choices=PRIMARY_USE_CHOICES, blank=True)
    no_of_branches = models.PositiveIntegerField(default=1)
    gstin = models.CharField(max_length=15, blank=True)
    referral_source = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    is_company_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Designation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='designations')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class Shift(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='shifts')
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('HD', 'Half Day'),
        ('L', 'Leave'),
        ('H', 'Holiday'),
        ('WO', 'Week Off'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    punch_in = models.DateTimeField(null=True, blank=True)
    punch_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default='P')
    latitude_in = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude_in = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude_out = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude_out = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.email} - {self.date} ({self.status})"

class RegularizationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='regularization_requests')
    attendance_date = models.DateField()
    reason = models.TextField()
    expected_punch_in = models.TimeField(null=True, blank=True)
    expected_punch_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.attendance_date} ({self.status})"

class LeaveType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='leave_types')
    name = models.CharField(max_length=100)
    total_days = models.PositiveIntegerField(default=12)
    carry_forward = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class UserLeaveBalance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    total_days = models.DecimalField(max_digits=5, decimal_places=2) # Base + Adjustments
    used_days = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'leave_type', 'year')

    def __str__(self):
        return f"{self.user.email} - {self.leave_type.name} ({self.year})"

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type_obj = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    leave_type = models.CharField(max_length=50) # Keep for backward compatibility or simple entry
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.leave_type} ({self.status})"

class Payroll(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payrolls')
    month = models.DateField() # Store as first day of month
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Processed')
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.month.strftime('%B %Y')}"

class EmployeeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    employee_code = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True, blank=True)
    aadhaar_last_4 = models.CharField(max_length=4, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, default='Employee') # Employee, Manager, HR/Admin

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_code})"

class LeavePolicy(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='leave_policy')
    max_leaves_per_year = models.PositiveIntegerField(default=30)
    accrual_policy = models.CharField(max_length=100, default='Monthly', choices=[('Monthly', 'Monthly'), ('Yearly', 'Yearly')])
    carry_forward_limit = models.PositiveIntegerField(default=5)
    approval_workflow = models.CharField(max_length=100, default='Single Level', choices=[('Single Level', 'Single Level'), ('Multi Level', 'Multi Level')])
    
    def __str__(self):
        return f"Policy for {self.company.name}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('Leave', 'Leave'),
        ('Attendance', 'Attendance'),
        ('Payroll', 'Payroll'),
        ('Employee', 'Employee'),
        ('System', 'System'),
        ('Announcement', 'Announcement'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} - {self.user.email} - {self.created_at}"

class Announcement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_announcements')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class NotificationSetting(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='notification_settings')
    enable_email = models.BooleanField(default=True)
    enable_sms = models.BooleanField(default=False)
    enable_push = models.BooleanField(default=False)
    enable_system = models.BooleanField(default=True)
    
    # Specific types
    leave_request_notif = models.BooleanField(default=True)
    payroll_alert_notif = models.BooleanField(default=True)
    attendance_alert_notif = models.BooleanField(default=True)
    employee_update_notif = models.BooleanField(default=True)
    system_update_notif = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.company.name}"


class PublicHoliday(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='public_holidays')
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} ({self.date})"
