from django.contrib.auth.models import User

import pytest

from volunteer import models


@pytest.fixture
def volunteer():
    user = User.objects.create_user(
        username="prez", first_name="The", last_name="Prez", email="theprez@whitehouse.gov", password="murica",
    )

    return models.Volunteer.objects.create(
        user=user,
        phone_number="1234567890",
        street_address="1600 Pennsylvania Ave",
        city="Washington",
        state="Washington, D.C.",
        zip_code="20500",
        country="United States",
    )


@pytest.mark.django_db
class TestVolunteer:
    def test_hours_are_zero_for_new_volunteer(self, volunteer):
        assert volunteer.hours() == 0

    def test_adding_timesheet_adds_hours(self, volunteer):
        models.Timesheet.objects.create(
            volunteer=volunteer, hours=42, notes="so much work",
        )

        assert volunteer.hours() == 42

    def test_points_are_double_the_hours(self, volunteer):
        hours = 42

        models.Timesheet.objects.create(
            volunteer=volunteer, hours=hours, notes="so much work",
        )

        assert volunteer.points() == hours * 2

    def test_service_hours_dont_accrue_points(self, volunteer):
        volunteer.type = "Service Hours"
        volunteer.save()

        models.Timesheet.objects.create(
            volunteer=volunteer, hours=42, notes="so much work",
        )

        assert volunteer.points() == 0

    def test_making_a_purchase_deducts_points(self, volunteer):
        hours = 42
        purchase = 32

        models.Timesheet.objects.create(
            volunteer=volunteer, hours=hours, notes="so much work",
        )

        models.Purchase.objects.create(
            volunteer=volunteer, points=purchase, description="big purchase",
        )

        assert volunteer.points() == (hours * 2) - purchase

    def test_is_member(self, volunteer):
        volunteer.type = "Drop-off Site Host"
        assert volunteer.is_member()
        volunteer.type = "Board Member"
        assert volunteer.is_member()

    def test_name(self, volunteer):
        assert volunteer.name() == "The Prez"
