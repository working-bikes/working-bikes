from django import test
from django.contrib.auth.models import User

from volunteer import models


class VolunteerTestCase(test.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='prez',
            first_name='The',
            last_name='Prez',
            email='theprez@whitehouse.gov',
            password='murica',
        )

        self.volunteer = models.Volunteer.objects.create(
            user=self.user,
            phone_number='1234567890',
            street_address='1600 Pennsylvania Ave',
            city='Washington',
            state='Washington, D.C.',
            zip_code='20500',
            country='United States',
        )

    def test_hours_are_zero_for_new_volunteer(self):
        self.assertEqual(0, self.volunteer.hours())

    def test_adding_timesheet_adds_hours(self):
        models.Timesheet.objects.create(
            volunteer=self.volunteer,
            hours=42,
            notes='so much work',
        )

        self.assertEqual(42, self.volunteer.hours())


    def test_points_are_double_the_hours(self):
        models.Timesheet.objects.create(
            volunteer=self.volunteer,
            hours=42,
            notes='so much work',
        )

        self.assertEqual(42 * 2, self.volunteer.points())

    def test_service_hours_dont_accrue_points(self):
        self.volunteer.type = 'Service Hours'
        self.volunteer.save()

        models.Timesheet.objects.create(
            volunteer=self.volunteer,
            hours=42,
            notes='so much work',
        )

        self.assertEqual(0, self.volunteer.points())

    def test_making_a_purchase_deducts_points(self):
        models.Timesheet.objects.create(
            volunteer=self.volunteer,
            hours=42,
            notes='so much work',
        )

        models.Purchase.objects.create(
            volunteer=self.volunteer,
            points=32,
            description='big purchase',
        )

        self.assertEqual((42 * 2) - 32, self.volunteer.points())

    def test_is_member(self):
        self.volunteer.type = 'Drop-off Site Host'
        self.assertTrue(self.volunteer.is_member())
        self.volunteer.type = 'Board Member'
        self.assertTrue(self.volunteer.is_member())

    def test_name(self):
        self.assertEqual('The Prez', self.volunteer.name())
