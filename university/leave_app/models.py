from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role, password=None):
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, role, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    roleType = models.TextChoices("Student", "Faculty")
    role = models.CharField(choices=roleType, max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Application(models.Model):
    class StatusType(models.TextChoices):
        APPROVED = "Approved"
        PENDING = "Pending"
        REJECTED = "Rejected"

    name = models.CharField(max_length=70)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # id foreign key
    university = models.CharField(max_length=70)
    program = models.CharField(max_length=70)
    studyType = models.TextChoices("Online", "Offline")
    study_mode = models.CharField(choices=studyType, max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_reason = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20, choices=StatusType.choices, default=StatusType.PENDING
    )

    def __str__(self):
        return self.name
