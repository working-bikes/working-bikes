from django.db import models
from django.contrib.auth.models import User

class Volunteer(models.Model):
	user = models.OneToOneField(User, unique=True)
	phone_number = models.CharField(max_length=15)
	street_address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=10)
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
