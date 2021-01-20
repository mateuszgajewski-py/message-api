from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjUserManager, \
	PermissionsMixin
from django.db import models


class UserManager(DjUserManager):
	def _create_user(self, email, password, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField('first name', max_length=150, blank=True)
	last_name = models.CharField('last name', max_length=150, blank=True)
	email = models.EmailField('email address', unique=True)
	is_staff = models.BooleanField('staff status', default=False)
	is_active = models.BooleanField('active', default=True)
	is_superuser = models.BooleanField('is superuser', default=False)
	date_joined = models.DateTimeField('date joined', auto_now_add=True)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'

	def get_full_name(self):
		"""
		Return the first_name plus the last_name, with a space in between.
		"""
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		"""Return the short name for the user."""
		return self.first_name
