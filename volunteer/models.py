from django.db import models
from django.contrib.auth.models import User

class Volunteer(models.Model):
	STATE_CHOICES = (
		('Alabama', 'AL'),
		('Alaska', 'AK'),
		('Arizona', 'AZ'),
		('Arkansas', 'AR'),
		('California', 'CA'),
		('Colorado', 'CO'),
		('Connecticut', 'CT'),
		('Delaware', 'DE'),
		('Florida', 'FL'),
		('Georgia', 'GA'),
		('Hawaii', 'HI'),
		('Idaho', 'ID'),
		('Illinois', 'IL'),
		('Indiana', 'IN'),
		('Iowa', 'IA'),
		('Kansas', 'KS'),
		('Kentucky', 'KY'),
		('Louisiana', 'LA'),
		('Maine', 'ME'),
		('Maryland', 'MD'),
		('Massachusetts', 'MA'),
		('Michigan', 'MI'),
		('Minnesota', 'MN'),
		('Mississippi', 'MS'),
		('Missouri', 'MO'),
		('Montana', 'MT'),
		('Nebraska', 'NE'),
		('Nevada', 'NV'),
		('New Hampshire', 'NH'),
		('New Jersey', 'NJ'),
		('New Mexico', 'NM'),
		('New York', 'NY'),
		('North Carolina', 'NC'),
		('North Dakota', 'ND'),
		('Ohio', 'OH'),
		('Oklahoma', 'OK'),
		('Oregon', 'OR'),
		('Pennsylvania', 'PA'),
		('Rhode Island', 'RI'),
		('South Carolina', 'SC'),
		('South Dakota', 'SD'),
		('Tennessee', 'TN'),
		('Texas', 'TX'),
		('Utah', 'UT'),
		('Vermont', 'VT'),
		('Virginia', 'VA'),
		('Washington', 'WA'),
		('West Virginia', 'WV'),
		('Wisconsin', 'WI'),
		('Wyoming', 'WY')
	)

	user = models.OneToOneField(User, unique=True)
	phone_number = models.CharField(max_length=15)
	street_address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=10, choices=STATE_CHOICES)
	zip_code = models.CharField(max_length=10)
	country = models.CharField(max_length=50)
	emergency_contact = models.CharField(max_length=50)
	emergency_contact_phone = models.CharField(max_length=15)

class Timesheet(models.Model):
	user = models.ForeignKey(User)
	day = models.DateField()
	hours = models.DecimalField(max_digits=4, decimal_places=2)
	notes = models.TextField()

	class Meta:
		unique_together = ('user', 'day',)

	def approved(self):
		try:
			approval = TimesheetApproval.objects.get(timesheet=self)
			return 'Approved'
		except TimesheetApproval.DoesNotExist:
			return 'Awaiting Approval'

class TimesheetApproval(models.Model):
	timesheet = models.OneToOneField(Timesheet, unique=True)
	approved_by = models.ForeignKey(User)

	def __unicode__(self):
		if self.approved_by.first_name != "" and self.approved_by.last_name != "":
			return 'Approved by %s %s' % (self.approved_by.first_name, self.approved_by.last_name)
		else:
			return 'Approved by %s' % self.approved_by.username
