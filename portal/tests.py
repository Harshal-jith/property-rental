from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Property, Booking
from .forms import RegistrationForm, BookingForm
import datetime

User = get_user_model()

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            full_name='Test Renter',
            phone='1234567890'
        )
        self.property = Property.objects.create(
            title='Test Modern Apartment',
            description='A beautiful test apartment in the city center.',
            rent=2500.00,
            city='Kochi',
            address='123 Main St, Kochi',
            bedrooms=2,
            bathrooms=2,
            area=1200,
            furnished=True,
            parking=True,
            available=True,
            main_image='properties/main/apartment_main.jpg'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpassword123'))
        self.assertEqual(self.user.full_name, 'Test Renter')

    def test_property_creation(self):
        self.assertEqual(self.property.title, 'Test Modern Apartment')
        self.assertEqual(self.property.city, 'Kochi')
        self.assertEqual(self.property.rent, 2500.00)

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            property=self.property,
            phone='1234567890',
            email='test@example.com',
            move_in_date=datetime.date.today() + datetime.timedelta(days=10),
            message='Looking forward to renting this!',
            status='Pending'
        )
        self.assertEqual(booking.status, 'Pending')
        self.assertEqual(booking.property, self.property)
        self.assertEqual(booking.user, self.user)


class FormTests(TestCase):
    def test_registration_form_valid(self):
        form_data = {
            'full_name': 'New User',
            'email': 'newuser@example.com',
            'phone': '1122334455',
            'password': 'safe_password123',
            'confirm_password': 'safe_password123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_mismatched_passwords(self):
        form_data = {
            'full_name': 'New User',
            'email': 'newuser@example.com',
            'phone': '1122334455',
            'password': 'passwordA',
            'confirm_password': 'passwordB'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_booking_form_past_date(self):
        form_data = {
            'name': 'Renter Name',
            'email': 'renter@example.com',
            'phone': '1122334455',
            'move_in_date': datetime.date.today() - datetime.timedelta(days=5),
            'message': 'Can I move in last week?'
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('move_in_date', form.errors)


class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            full_name='Test Renter'
        )
        self.property = Property.objects.create(
            title='Test Villa',
            description='Test description.',
            rent=3000.00,
            city='Kochi',
            address='123 Main St',
            bedrooms=3,
            bathrooms=2,
            area=1500,
            furnished=True,
            parking=True,
            available=True,
            main_image='properties/main/villa_main.jpg'
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/home.html')

    def test_listings_view_filters(self):
        self.client.login(email='test@example.com', password='testpassword123')
        response = self.client.get(reverse('listings'), {'city': 'Kochi', 'bedrooms': '3'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Villa')

    def test_unauthenticated_listings_redirects(self):
        response = self.client.get(reverse('listings'))
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_unauthenticated_detail_redirects(self):
        response = self.client.get(reverse('property_detail', kwargs={'pk': self.property.pk}))
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_unauthenticated_dashboard_redirects(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_authenticated_dashboard_view(self):
        self.client.login(email='test@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal/dashboard.html')


class BookingEmailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='renter@example.com',
            password='testpassword123',
            full_name='Alice Smith'
        )
        self.property = Property.objects.create(
            title='Test Sea View Penthouse',
            description='Test descriptions.',
            rent=5000.00,
            city='Trivandrum',
            address='Skyline road, Trivandrum',
            bedrooms=3,
            bathrooms=3,
            area=2500,
            furnished=True,
            parking=True,
            available=True,
            main_image='properties/main/penthouse.jpg'
        )

    def test_email_sent_on_booking_creation(self):
        from django.core import mail
        
        # Initially outbox should be empty
        self.assertEqual(len(mail.outbox), 0)
        
        # Create a new booking request
        booking = Booking.objects.create(
            user=self.user,
            property=self.property,
            phone='9876543210',
            email='renter@example.com',
            move_in_date=datetime.date.today() + datetime.timedelta(days=5),
            message='I want this penthouse!',
            status='Pending'
        )
        
        # Verify one confirmation email was dispatched
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f"Booking Request Submitted: {self.property.title}")
        self.assertEqual(mail.outbox[0].to, ['renter@example.com'])
        self.assertIn('Pending Review', mail.outbox[0].body)

    def test_email_sent_on_booking_approval(self):
        from django.core import mail
        
        booking = Booking.objects.create(
            user=self.user,
            property=self.property,
            phone='9876543210',
            email='renter@example.com',
            move_in_date=datetime.date.today() + datetime.timedelta(days=5),
            status='Pending'
        )
        
        # Clear outbox (1 email sent on creation)
        mail.outbox.clear()
        
        # Approve booking status
        booking.status = 'Approved'
        booking.save()
        
        # Verify status update email was dispatched
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f"Booking Request Update: {self.property.title} - Approved")
        self.assertIn('Approved / Confirmed', mail.outbox[0].body)

    def test_email_sent_on_booking_rejection(self):
        from django.core import mail
        
        booking = Booking.objects.create(
            user=self.user,
            property=self.property,
            phone='9876543210',
            email='renter@example.com',
            move_in_date=datetime.date.today() + datetime.timedelta(days=5),
            status='Pending'
        )
        
        # Clear outbox (1 email sent on creation)
        mail.outbox.clear()
        
        # Reject booking status
        booking.status = 'Rejected'
        booking.save()
        
        # Verify status update email was dispatched
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, f"Booking Request Update: {self.property.title} - Rejected")
        self.assertIn('Declined', mail.outbox[0].body)
