from django.contrib import admin
from .models import Company, CustomUser, EmployeeProfile, Department, Shift, Branch, Designation, Attendance, LeaveRequest, Payroll, PublicHoliday

admin.site.register(Company)
admin.site.register(CustomUser)
admin.site.register(EmployeeProfile)
admin.site.register(Department)
admin.site.register(Shift)
admin.site.register(Branch)
admin.site.register(Designation)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
admin.site.register(Payroll)
admin.site.register(PublicHoliday)
