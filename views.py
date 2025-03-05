# Create your views here.
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *# import all models from models.py using *
from datetime import datetime # import date and time models

# register new student for library
def registration(request):
    if request.method == "POST":
        # Collect form data
        name = request.POST.get("name")
        mobile_number = request.POST.get("mobile_number")
        aadhar_number = request.POST.get("aadhar_number")
        address = request.POST.get("address")
        slot_number = request.POST.get("slot_number")
        seat_number = request.POST.get("seat_number")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        library_id = request.POST.get("library")  # Library selected by the user

        try:
            # Convert start_date and end_date to datetime.date objects
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            # Check if student already exists or create a new one
            student, created = Student.objects.get_or_create(
                mobile_number=mobile_number,
                defaults={
                    "name": name,
                    "aadhar_number": aadhar_number,
                    "address": address,
                }
            )

            # If the student exists but details differ, update them
            if not created:
                student.name = name
                student.aadhar_number = aadhar_number
                student.address = address
                student.save()

            # Assign the library to the student
            library = Library.objects.get(id=library_id)
            student.library = library
            student.save()

            # Check if the student already has a registration
            if Registration.objects.filter(mobile_number=student).exists():
                messages.error(request, "Student is already registered!")
                return redirect("registration")

            # Create a new registration
            registration = Registration(
                mobile_number=student,
                slot_number=slot_number,
                seat_number=seat_number,
                start_date=start_date,
                end_date=end_date
            )
            registration.save()

            messages.success(request, "Registration successful!")
        except ValueError as e:
            messages.error(request, f"Invalid date format: {e}")
        except Library.DoesNotExist:
            messages.error(request, "Selected library does not exist!")
        except Exception as e:
            messages.error(request, f"Error: {e}")

        return redirect("registration")

    # Fetch libraries for the dropdown
    libraries = Library.objects.all()

    return render(request, "registration.html", {"libraries": libraries})

# Add new library from here
def library_registration(request):
    if request.method == "POST":
        owner_name = request.POST.get("owner_name")
        mobile_number = request.POST.get("mobile_number")
        aadhar_number = request.POST.get("aadhar_number")
        dob = request.POST.get("dob")  # DOB input in DDMMYYYY format
        library_name = request.POST.get("library_name")
        seat_capacity = request.POST.get("seat_capacity")
        library_address = request.POST.get("library_address")

        # Validate mobile number length (must be 10 digits)
        if len(mobile_number) != 10 or not mobile_number.isdigit():
            messages.error(request, "Please enter a valid 10-digit mobile number.")
            return redirect("library_registration")

        # Validate Aadhar number length (must be 12 digits)
        if len(aadhar_number) != 12 or not aadhar_number.isdigit():
            messages.error(request, "Please enter a valid 12-digit Aadhar number.")
            return redirect("library_registration")

        # Validate DOB format (DDMMYYYY - exactly 8 digits)
        if not re.match(r'^\d{8}$', dob):
            messages.error(request, "Please enter a valid Date of Birth in DDMMYYYY format.")
            return redirect("library_registration")

        # Check if a library with the same mobile number already exists
        if Library.objects.filter(mobile_number=mobile_number).exists():
            messages.error(request, "Library with this mobile number already exists!")
            return redirect("library_registration")

        # Check if a library with the same Aadhar number already exists
        if Library.objects.filter(aadhar_number=aadhar_number).exists():
            messages.error(request, "Library with this Aadhar number already exists!")
            return redirect("library_registration")

        # Validate seat capacity (must be a positive integer)
        try:
            seat_capacity = int(seat_capacity)
            if seat_capacity <= 0:
                raise ValueError("Seat capacity must be a positive number.")
        except ValueError:
            messages.error(request, "Please enter a valid seat capacity.")
            return redirect("library_registration")

        # Create a new library entry
        Library.objects.create(
            owner_name=owner_name,
            mobile_number=mobile_number,
            aadhar_number=aadhar_number,
            dob=dob,  # Store DOB as string in DDMMYYYY format
            library_name=library_name,
            seat_capacity=seat_capacity,
            library_address=library_address,
        )
        messages.success(request, "Library registered successfully!")
        return redirect("library_registration")

    return render(request, "library_registration.html")

# View for displaying the list of libraries and adding a new library
def library(request):
    if request.method == "POST":
        owner_name = request.POST.get("owner_name")
        mobile_number = request.POST.get("mobile_number")
        library_name = request.POST.get("library_name")
        seat_capacity = request.POST.get("seat_capacity")
        library_address = request.POST.get("library_address")

        # Check if a library with the same mobile number already exists
        if Library.objects.filter(mobile_number=mobile_number).exists():
            messages.error(request, "Library with this mobile number already exists!")
            return redirect("library")

        # Create a new library entry
        Library.objects.create(
            owner_name=owner_name,
            mobile_number=mobile_number,
            library_name=library_name,
            seat_capacity=seat_capacity,
            library_address=library_address,
        )
        messages.success(request, "Library registered successfully!")
        return redirect("library")

    # Get all libraries to display
    libraries = Library.objects.all()
    return render(request, "library.html", {"libraries": libraries})

# View for verification before update or delete action
def verify_action(request, library_id, action):
    library = get_object_or_404(Library, id=library_id)

    if request.method == "POST":
        aadhar_number = request.POST.get("aadhar_number")
        dob = request.POST.get("dob")

        # Verify Aadhar number and DOB match
        if aadhar_number == library.aadhar_number and dob == library.dob:
            if action == "update":
                return redirect("update_library", library_id=library_id)
            elif action == "delete":
                return redirect("delete_library", library_id=library_id)
        else:
            messages.error(request, "Aadhar Number or DOB does not match! Please try again.")
            return redirect("verify_action", library_id=library_id, action=action)

    return render(request, "verification.html", {"library": library, "action": action})

# View for updating library information
def update_library(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    
    if request.method == "POST":
        library.owner_name = request.POST.get("owner_name")
        library.mobile_number = request.POST.get("mobile_number")
        library.aadhar_number = request.POST.get("aadhar_number")  # Handle Aadhar Number
        library.dob = request.POST.get("dob")  # Handle DOB
        library.library_name = request.POST.get("library_name")
        library.seat_capacity = request.POST.get("seat_capacity")
        library.library_address = request.POST.get("library_address")

        # Check for unique mobile number (excluding current library)
        if Library.objects.filter(mobile_number=library.mobile_number).exclude(id=library_id).exists():
            messages.error(request, "Another library with this mobile number already exists!")
            return redirect("update_library", library_id=library_id)

        library.save()
        messages.success(request, "Library updated successfully!")
        
        # Redirect with countdown
        return render(request, "update_library.html", {
            "library": library,
            "redirect_countdown": True  # Pass countdown flag to the template
        })

    return render(request, "update_library.html", {"library": library})

# View for deleting a library
def delete_library(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    library.delete()
    messages.success(request, "Library deleted successfully!")
    return redirect("library")

def seat(request):
    selected_library_id = request.POST.get("library_id")
    selected_library = None
    seat_data = {}

    if selected_library_id:
        selected_library = Library.objects.get(id=selected_library_id)
        registrations = Registration.objects.filter(mobile_number__library=selected_library)

        # Initialize seat data with all slots as vacant
        for seat in range(1, selected_library.seat_capacity + 1):
            seat_data[seat] = [{"status": "vacant", "student_id": None} for _ in range(3)]  # Three slots per seat

        # Update seat data based on registrations
        for reg in registrations:
            seat_number = reg.seat_number
            slot_number = reg.slot_number - 1  # Convert slot to zero-based index
            status = "occupied" if reg.status else "vacant"
            if seat_number in seat_data:
                seat_data[seat_number][slot_number] = {"status": status, "registration": reg}


    return render(request, "seat.html", {
        "libraries": Library.objects.all(),
        "selected_library": selected_library,
        "selected_library_id": selected_library_id,
        "seat_data": seat_data,
    })

def student_details(request, student_id):
    # Fetch registration using the ID (primary key)
    registration = get_object_or_404(Registration, id=student_id)

    # Access the student details related to the registration
    student = registration.mobile_number  # Assuming mobile_number links to Student
    
    return render(request, 'student.html', {'registration': registration, 'student': student})
