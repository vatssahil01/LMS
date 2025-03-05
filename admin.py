from django.contrib import admin
from library.models import Library, Student, Registration

# Register the Student model with customized admin options
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_number', 'aadhar_number', 'address')  # Fields to display in the list view
    search_fields = ('name', 'mobile_number', 'aadhar_number')  # Add search functionality for these fields
    list_filter = ('address',)  # Add a filter for address (if relevant)
    ordering = ('name',)  # Order the students by name

# Register the Registration model with customized admin options
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'mobile_number_display', 'slot_number', 'seat_number', 'start_date', 'end_date', 'status')  # Fields to display
    list_filter = ('status', 'slot_number')  # Add filters for status and slot number
    search_fields = ('mobile_number__name', 'mobile_number__mobile_number', 'seat_number')  # Add search functionality for name, mobile, and seat number
    ordering = ('-start_date',)  # Order registrations by start date (most recent first)

    def student_name(self, obj):
        return obj.mobile_number.name  # Access the student's name via the foreign key

    def mobile_number_display(self, obj):
        return obj.mobile_number.mobile_number  # Access the student's mobile number via the foreign key

    # Optional: Add display names for the custom fields
    student_name.short_description = 'Name'
    mobile_number_display.short_description = 'Mobile Number'

# Register the Library model with customized admin options
@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = (
        'owner_name', 'mobile_number', 'aadhar_number', 'dob', 'library_name', 
        'seat_capacity', 'library_address'
    )  # Display all relevant fields in the list view
    search_fields = (
        'owner_name', 'mobile_number', 'library_name', 'aadhar_number'
    )  # Allow searching by these fields
    list_filter = ('library_name',)  # Add a filter for library name
    ordering = ('library_name',)  # Order libraries by library name
