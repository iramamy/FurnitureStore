from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        """
        Create a new user with the given first name, last name, username, email, and password.

        Args:
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.

        Raises:
            ValueError: If the email or username is not provided.

        Returns:
            Account: The newly created user object.

        """

        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        """
        Create a superuser with the given first name, last name, username, email, and password.

        Args:
            first_name (str): The first name of the superuser.
            last_name (str): The last name of the superuser.
            username (str): The username of the superuser.
            email (str): The email address of the superuser.
            password (str): The password for the superuser.

        Returns:
            Account: The newly created superuser object.
        """

        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_super_user = True
        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username= models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_super_user = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        """
        Returns a string representation of the email attribute of the current object.

        :return: A string representing the email attribute of the current object.
        :rtype: str
        """

        return str(self.email)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission.

        Args:
            perm (str): The permission to check.
            obj (Optional[Any]): The object to check the permission against. Defaults to None.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """

        return self.is_admin

    def has_module_perms(self, add_label):
        """
        Check if the user has permissions for a specific app.

        Args:
            app_label (str): The label of the app to check permissions for.

        Returns:
            bool: True if the user has permissions for the app, False otherwise.
        """

        return True
    
    @property
    def is_authenticated(self):
        """
        Check if the user is authenticated.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return True

    @property
    def is_anonymous(self):
        """
        Check if the user is anonymous.

        Returns:
            bool: False, as this user is not anonymous.
        """

        return False

class UserProfile(models.Model):

    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile/')
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.user.first_name)
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"
    