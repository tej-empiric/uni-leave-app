import re
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyUser, Application
from django.contrib.auth.hashers import check_password
from .backends import EmailBackend
from django.contrib.auth.hashers import make_password


def loginPage(request):

    if request.method == "POST":
        email = request.POST.get("email")
        pass1 = request.POST.get("password")

        user = EmailBackend.authenticate(
            request,
            username=email,
            password=pass1,
        )
        # print("User:", user)

        if user is not None:
            user.backend = "leave_app.backends.EmailBackend"

            login(request, user)
            return redirect("user/")
        else:
            messages.info(request, "Email or password is incorrect!")

    return render(request, "leave_app/login.html")


def register(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        role = request.POST.get("role")

        password_pattern = (
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*_=+-]).{8,16}$"
        )

        if not re.match(password_pattern, pass1):
            messages.info(
                request,
                "Passwords must contain one special character, one upper and one lower character and length more than 8.",
            )

        elif pass1 != pass2:
            messages.info(request, "Passwords do not match")
        else:
            if MyUser.objects.filter(email=request.POST["email"]).exists():
                messages.info(request, "User already registered")
            else:
                new_user = MyUser.objects.create(
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    password=make_password(pass1),
                    role=role,
                )
                new_user.save()
                messages.success(request, "Registration done successfully.")
                # login(request, new_user)
                return redirect("/")

    return render(request, "leave_app/register.html")


@login_required
def user(request):

    current_user = request.user
    fullname = current_user.get_full_name()
    role = MyUser.objects.filter(email=current_user.email).values_list(
        "role", flat=True
    )

    if request.method == "POST":
        name = request.POST.get("name")
        university = request.POST.get("university")
        program = request.POST.get("program")
        study_mode = request.POST.get("study")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        reason = request.POST.get("reason")

        application = Application.objects.create(
            name=name,
            user=request.user,
            university=university,
            program=program,
            study_mode=study_mode,
            start_date=start_date,
            end_date=end_date,
            leave_reason=reason,
        )

        application.save()

        messages.success(request, "Application submitted successfully.")

        return redirect("leave_status/")

    student_app = Application.objects.all()  # for faculty page

    return render(
        request,
        "leave_app/user.html",
        {"name": role, "fullname": fullname, "student_app": student_app},
    )


@login_required
def change_status(request, id):
    if request.method == "POST":
        app = Application.objects.get(pk=id)
        if "approve" in request.POST:
            app.status = "Approved"
        elif "reject" in request.POST:
            app.status = "Rejected"

        app.save()
        return redirect("/user/")

    return render(request, "leave_app/user.html")


@login_required
def leaveStatus(request):
    current_user = request.user
    fullname = current_user.get_full_name()
    application = Application.objects.filter(user=request.user)
    return render(
        request,
        "leave_app/leave_status.html",
        {
            "application": application,
            "fullname": fullname,
        },
    )


def forget(request):
    pass


@login_required
def logoutPage(request):
    logout(request)
    return redirect("/")
