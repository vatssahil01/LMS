
# Create your models here.
from django.db import models
from datetime import date

# Library Table for storing library details
class Library(models.Model):
    owner_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)
    aadhar_number = models.CharField(max_length=12, unique=True, default='000000000000')
    dob = models.CharField(max_length=8, default='01012001', null=True, blank=True)
    library_name = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    library_address = models.TextField()

    def __str__(self):
        return self.library_name

# Student Table for storing student details
class Student(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, primary_key=True)
    aadhar_number = models.CharField(max_length=12, unique=True)
    address = models.TextField()
    library = models.ForeignKey('Library', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.name


# Registration Table for storing registration details
class Registration(models.Model):
    mobile_number = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="registration")
    slot_number = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=True)  # Active by default

    def save(self, *args, **kwargs):
        # Automatically set status based on end_date
        self.status = self.end_date >= date.today()
        super(Registration, self).save(*args, **kwargs)

    def __str__(self):
        return f"Registration for {self.mobile_number.name} - Slot {self.slot_number}"


