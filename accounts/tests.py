from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user(self):
        """Test creating a regular user with email and password"""
        email = 'test@example.com'
        password = 'testpass123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_without_email(self):
        """Test creating a user without email raises ValueError"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpass123')

        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password='testpass123')

    def test_create_user_normalize_email(self):
        """Test email is normalized when creating user"""
        email = 'test@EXAMPLE.com'
        user = User.objects.create_user(email=email, password='testpass123')
        self.assertEqual(user.email, email.lower())

    def test_create_superuser(self):
        """Test creating a superuser"""
        email = 'admin@example.com'
        password = 'testpass123'
        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_with_invalid_flags(self):
        """Test creating superuser with invalid is_staff or is_superuser flags"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', password='testpass123', is_staff=False
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com', password='testpass123', is_superuser=False
            )


class UserModelTests(TestCase):
    def setUp(self):
        self.user_data = {'email': 'test@example.com', 'password': 'testpass123'}

    def test_user_creation(self):
        """Test creating a user with all required fields"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertIsNotNone(user.date_joined)
        self.assertIsNone(user.last_login)

    def test_email_unique_constraint(self):
        """Test that email must be unique"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)

    def test_email_max_length(self):
        """Test email max length validation"""
        long_email = 'a' * 245 + '@example.com'  # 255 characters (exceeds 254)
        with self.assertRaises(ValidationError):
            user = User(email=long_email, password='testpass123')
            user.full_clean()

    def test_username_is_none(self):
        """Test that username value is None"""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNone(user.username)

    def test_required_fields(self):
        """Test that REQUIRED_FIELDS is empty and USERNAME_FIELD is email"""
        self.assertEqual(User.REQUIRED_FIELDS, [])
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_date_joined_auto_set(self):
        """Test that date_joined is automatically set"""
        before = timezone.now()
        user = User.objects.create_user(**self.user_data)
        after = timezone.now()

        self.assertTrue(before <= user.date_joined <= after)

    def test_last_login_nullable(self):
        """Test that last_login can be null"""
        user = User.objects.create_user(**self.user_data)
        self.assertIsNone(user.last_login)

        # Test updating last_login
        test_time = timezone.now()
        user.last_login = test_time
        user.save()
        self.assertEqual(user.last_login, test_time)
