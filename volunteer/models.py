import datetime

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Task(models.Model):
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
        ('Wyoming', 'WY'),
        ('Washington, D.C.', 'Washington, D.C.'),
        ('Other', 'Other'),
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
        ('Myanmar', 'Myanmar',),
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
        ('Service Hours', 'Service Hours'),
        ('Staff', 'Staff'),
        ('Board Member', 'Board Member'),
        ('Drop-off Site Host', 'Drop-off Site Host'),
    )

    user = models.OneToOneField(User, unique=True)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='United States')
    emergency_contact = models.CharField(max_length=50, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    preferred_tasks = models.ManyToManyField(Task, null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=VOLUNTEER_TYPE_CHOICES, default='Volunteer')

    class Meta:
        ordering = ['user__first_name']

    def hours(self):
        total_hours = self.timesheet_set.aggregate(Sum('hours')).get('hours__sum', 0.0)
        if total_hours is None:
            total_hours = 0
        return total_hours

    def points(self):
        if self.type == 'Service Hours':
            return 0

        hour_sum = self.hours()
        purchase_sum = self.purchase_set.aggregate(Sum('points')).get('points__sum', 0)

        if purchase_sum is None:
            purchase_sum = 0
        if hour_sum is None:
            hour_sum = 0

        return int(hour_sum) * 2 - purchase_sum

    def is_member(self):
        if any([
                    self.type in ['Drop-off Site Host', 'Board Member'],
                    self.type == 'Staff' and self.membership_length_months() > 6,
                    self.six_month_avg_hours() >= 4,
                    self.total_hours_in_last_n_days(365) >= 48
        ]):
            return True
        else:
            return False

    is_member.boolean = True
    is_member.short_description = 'Member?'

    def membership_length_months(self):
        delta = datetime.datetime.now() - self.user.date_joined.replace(tzinfo=None)
        delta_total_seconds = (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 10 ** 6) / 10 ** 6
        return delta_total_seconds / 60.0 / 60 / 24 / 30

    def total_hours_in_last_n_days(self, num_days):
        timesheets = self.timesheet_set.filter(day__gt=datetime.date.today() - datetime.timedelta(days=num_days))
        total = 0
        for timesheet in timesheets:
            if timesheet.approved():
                total += timesheet.hours
        return total

    def six_month_avg_hours(self):
        return self.total_hours_in_last_n_days(180) / 6

    def name(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)

    def __unicode__(self):
        return self.name()


class Timesheet(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    day = models.DateField(default=datetime.date.today)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    notes = models.TextField()
    task = models.ForeignKey(Task, blank=True, null=True)
    from_event = models.BooleanField(default=False)

    def approved(self):
        try:
            TimesheetApproval.objects.get(timesheet=self)
            return True
        except TimesheetApproval.DoesNotExist:
            return False

    approved.boolean = True

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


class Purchase(models.Model):
    volunteer = models.ForeignKey(Volunteer)
    date = models.DateTimeField(default=datetime.datetime.now)
    points = models.IntegerField()
    description = models.TextField()

    class Meta:
        ordering = ['volunteer__user__first_name']

    def approved(self):
        try:
            PurchaseApproval.objects.get(purchase=self)
            return True
        except PurchaseApproval.DoesNotExist:
            return False

    approved.boolean = True


class PurchaseApproval(models.Model):
    purchase = models.OneToOneField(Purchase, unique=True)
    approved_by = models.ForeignKey(User)

    def __unicode__(self):
        if self.approved_by.first_name != '' and self.approved_by.last_name != '':
            return 'Approved by %s %s' % (self.approved_by.first_name, self.approved_by.last_name)
        else:
            return 'Approved by %s' % self.approved_by.username