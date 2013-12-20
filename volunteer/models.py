from django.db import models
from django.contrib.auth.models import User

class VolunteerTask(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField()
	members_only = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

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

	COUNTRY_CHOICES = (
		('Afghanistan', 'Afghanistan'),
		('Albania', 'Albania'),
		('Algeria', 'Algeria'),
		('Andorra', 'Andorra'),
		('Angola', 'Angola'),
		('Antigua & Deps', 'Antigua & Deps'),
		('Argentina', 'Argentina'),
		('Armenia', 'Armenia'),
		('Australia', 'Australia'),
		('Austria', 'Austria'),
		('Azerbaijan', 'Azerbaijan'),
		('Bahamas', 'Bahamas'),
		('Bahrain', 'Bahrain'),
		('Bangladesh', 'Bangladesh'),
		('Barbados', 'Barbados'),
		('Belarus', 'Belarus'),
		('Belgium', 'Belgium'),
		('Belize', 'Belize'),
		('Benin', 'Benin'),
		('Bhutan', 'Bhutan'),
		('Bolivia', 'Bolivia'),
		('Bosnia Herzegovina', 'Bosnia Herzegovina'),
		('Botswana', 'Botswana'),
		('Brazil', 'Brazil'),
		('Brunei', 'Brunei'),
		('Bulgaria', 'Bulgaria'),
		('Burkina', 'Burkina'),
		('Burundi', 'Burundi'),
		('Cambodia', 'Cambodia'),
		('Cameroon', 'Cameroon'),
		('Canada', 'Canada'),
		('Cape Verde', 'Cape Verde'),
		('Central African Rep', 'Central African Rep'),
		('Chad', 'Chad'),
		('Chile', 'Chile'),
		('China', 'China'),
		('Colombia', 'Colombia'),
		('Comoros', 'Comoros'),
		('Congo', 'Congo'),
		('Congo (Democratic Republic)', 'Congo (Democratic Republic)'),
		('Costa Rica', 'Costa Rica'),
		('Croatia', 'Croatia'),
		('Cuba', 'Cuba'),
		('Cyprus', 'Cyprus'),
		('Czech Republic', 'Czech Republic'),
		('Denmark', 'Denmark'),
		('Djibouti', 'Djibouti'),
		('Dominica', 'Dominica'),
		('Dominican Republic', 'Dominican Republic'),
		('East Timor', 'East Timor'),
		('Ecuador', 'Ecuador'),
		('Egypt', 'Egypt'),
		('El Salvador', 'El Salvador'),
		('Equatorial Guinea', 'Equatorial Guinea'),
		('Eritrea', 'Eritrea'),
		('Estonia', 'Estonia'),
		('Ethiopia', 'Ethiopia'),
		('Fiji', 'Fiji'),
		('Finland', 'Finland'),
		('France', 'France'),
		('Gabon', 'Gabon'),
		('Gambia', 'Gambia'),
		('Georgia', 'Georgia'),
		('Germany', 'Germany'),
		('Ghana', 'Ghana'),
		('Greece', 'Greece'),
		('Grenada', 'Grenada'),
		('Guatemala', 'Guatemala'),
		('Guinea', 'Guinea'),
		('Guinea-Bissau', 'Guinea-Bissau'),
		('Guyana', 'Guyana'),
		('Haiti', 'Haiti'),
		('Honduras', 'Honduras'),
		('Hungary', 'Hungary'),
		('Iceland', 'Iceland'),
		('India', 'India'),
		('Indonesia', 'Indonesia'),
		('Iran', 'Iran'),
		('Iraq', 'Iraq'),
		('Ireland', 'Ireland'),
		('Israel', 'Israel'),
		('Italy', 'Italy'),
		('Ivory Coast', 'Ivory Coast'),
		('Jamaica', 'Jamaica'),
		('Japan', 'Japan'),
		('Jordan', 'Jordan'),
		('Kazakhstan', 'Kazakhstan'),
		('Kenya', 'Kenya'),
		('Kiribati', 'Kiribati'),
		('Korea North', 'Korea North'),
		('Korea South', 'Korea South'),
		('Kosovo', 'Kosovo'),
		('Kuwait', 'Kuwait'),
		('Kyrgyzstan', 'Kyrgyzstan'),
		('Laos', 'Laos'),
		('Latvia', 'Latvia'),
		('Lebanon', 'Lebanon'),
		('Lesotho', 'Lesotho'),
		('Liberia', 'Liberia'),
		('Libya', 'Libya'),
		('Liechtenstein', 'Liechtenstein'),
		('Lithuania', 'Lithuania'),
		('Luxembourg', 'Luxembourg'),
		('Macedonia', 'Macedonia'),
		('Madagascar', 'Madagascar'),
		('Malawi', 'Malawi'),
		('Malaysia', 'Malaysia'),
		('Maldives', 'Maldives'),
		('Mali', 'Mali'),
		('Malta', 'Malta'),
		('Marshall Islands', 'Marshall Islands'),
		('Mauritania', 'Mauritania'),
		('Mauritius', 'Mauritius'),
		('Mexico', 'Mexico'),
		('Micronesia', 'Micronesia'),
		('Moldova', 'Moldova'),
		('Monaco', 'Monaco'),
		('Mongolia', 'Mongolia'),
		('Montenegro', 'Montenegro'),
		('Morocco', 'Morocco'),
		('Mozambique', 'Mozambique'),
		('Myanmar',  'Myanmar',),
		('Namibia', 'Namibia'),
		('Nauru', 'Nauru'),
		('Nepal', 'Nepal'),
		('Netherlands', 'Netherlands'),
		('New Zealand', 'New Zealand'),
		('Nicaragua', 'Nicaragua'),
		('Niger', 'Niger'),
		('Nigeria', 'Nigeria'),
		('Norway', 'Norway'),
		('Oman', 'Oman'),
		('Pakistan', 'Pakistan'),
		('Palau', 'Palau'),
		('Panama', 'Panama'),
		('Papua New Guinea', 'Papua New Guinea'),
		('Paraguay', 'Paraguay'),
		('Peru', 'Peru'),
		('Philippines', 'Philippines'),
		('Poland', 'Poland'),
		('Portugal', 'Portugal'),
		('Qatar', 'Qatar'),
		('Romania', 'Romania'),
		('Russian Federation', 'Russian Federation'),
		('Rwanda', 'Rwanda'),
		('St Kitts & Nevis', 'St Kitts & Nevis'),
		('St Lucia', 'St Lucia'),
		('Saint Vincent & the Grenadines', 'Saint Vincent & the Grenadines'),
		('Samoa', 'Samoa'),
		('San Marino', 'San Marino'),
		('Sao Tome & Principe', 'Sao Tome & Principe'),
		('Saudi Arabia', 'Saudi Arabia'),
		('Senegal', 'Senegal'),
		('Serbia', 'Serbia'),
		('Seychelles', 'Seychelles'),
		('Sierra Leone', 'Sierra Leone'),
		('Singapore', 'Singapore'),
		('Slovakia', 'Slovakia'),
		('Slovenia', 'Slovenia'),
		('Solomon Islands', 'Solomon Islands'),
		('Somalia', 'Somalia'),
		('South Africa', 'South Africa'),
		('South Sudan', 'South Sudan'),
		('Spain', 'Spain'),
		('Sri Lanka', 'Sri Lanka'),
		('Sudan', 'Sudan'),
		('Suriname', 'Suriname'),
		('Swaziland', 'Swaziland'),
		('Sweden', 'Sweden'),
		('Switzerland', 'Switzerland'),
		('Syria', 'Syria'),
		('Taiwan', 'Taiwan'),
		('Tajikistan', 'Tajikistan'),
		('Tanzania', 'Tanzania'),
		('Thailand', 'Thailand'),
		('Togo', 'Togo'),
		('Tonga', 'Tonga'),
		('Trinidad & Tobago', 'Trinidad & Tobago'),
		('Tunisia', 'Tunisia'),
		('Turkey', 'Turkey'),
		('Turkmenistan', 'Turkmenistan'),
		('Tuvalu', 'Tuvalu'),
		('Uganda', 'Uganda'),
		('Ukraine', 'Ukraine'),
		('United Arab Emirates', 'United Arab Emirates'),
		('United Kingdom', 'United Kingdom'),
		('United States', 'United States'),
		('Uruguay', 'Uruguay'),
		('Uzbekistan', 'Uzbekistan'),
		('Vanuatu', 'Vanuatu'),
		('Vatican City', 'Vatican City'),
		('Venezuela', 'Venezuela'),
		('Vietnam', 'Vietnam'),
		('Yemen', 'Yemen'),
		('Zambia', 'Zambia'),
		('Zimbabwe', 'Zimbabwe'),
	)

	VOLUNTEER_TYPE_CHOICES = (
		('Volunteer', 'Volunteer'),
		('Board Member', 'Board Member'),
		('Staff', 'Staff'),
		('Drop-off Site Host', 'Drop-off Site Host'),
	)

	user = models.OneToOneField(User, unique=True)
	phone_number = models.CharField(max_length=15)
	street_address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=10, choices=STATE_CHOICES)
	zip_code = models.CharField(max_length=10)
	country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='United States')
	emergency_contact = models.CharField(max_length=50, null=True, blank=True)
	emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
	preferred_tasks = models.ManyToManyField(VolunteerTask, null=True, blank=True)
	type = models.CharField(max_length=50, choices=VOLUNTEER_TYPE_CHOICES, default='Volunteer')
	
	def __unicode__(self):
		return '%s %s' % (user.first_name, user.last_name)

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

	def __unicode__(self):
		return str(self.day)

class TimesheetApproval(models.Model):
	timesheet = models.OneToOneField(Timesheet, unique=True)
	approved_by = models.ForeignKey(User)

	def __unicode__(self):
		if self.approved_by.first_name != '' and self.approved_by.last_name != '':
			return 'Approved by %s %s' % (self.approved_by.first_name, self.approved_by.last_name)
		else:
			return 'Approved by %s' % self.approved_by.username

class Event(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField()

class EventTask(models.Model):
	task = models.ForeignKey(VolunteerTask)
	event = models.ForeignKey(Event)
	volunteers = models.ManyToManyField(Volunteer)

