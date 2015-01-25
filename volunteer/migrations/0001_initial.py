# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'VolunteerTask'
        db.create_table(u'volunteer_volunteertask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('members_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'volunteer', ['VolunteerTask'])

        # Adding model 'Volunteer'
        db.create_table(u'volunteer_volunteer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.CharField')(default='United States', max_length=50)),
            ('emergency_contact', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('emergency_contact_phone',
             self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('skills', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Volunteer', max_length=50)),
        ))
        db.send_create_signal(u'volunteer', ['Volunteer'])

        # Adding M2M table for field preferred_tasks on 'Volunteer'
        m2m_table_name = db.shorten_name(u'volunteer_volunteer_preferred_tasks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('volunteer', models.ForeignKey(orm[u'volunteer.volunteer'], null=False)),
            ('volunteertask', models.ForeignKey(orm[u'volunteer.volunteertask'], null=False))
        ))
        db.create_unique(m2m_table_name, ['volunteer_id', 'volunteertask_id'])

        # Adding model 'Timesheet'
        db.create_table(u'volunteer_timesheet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volunteer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['volunteer.Volunteer'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('hours', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'volunteer', ['Timesheet'])

        # Adding unique constraint on 'Timesheet', fields ['volunteer', 'day']
        db.create_unique(u'volunteer_timesheet', ['volunteer_id', 'day'])

        # Adding model 'TimesheetApproval'
        db.create_table(u'volunteer_timesheetapproval', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timesheet',
             self.gf('django.db.models.fields.related.OneToOneField')(to=orm['volunteer.Timesheet'], unique=True)),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'volunteer', ['TimesheetApproval'])

        # Adding model 'Event'
        db.create_table(u'volunteer_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'volunteer', ['Event'])

        # Adding model 'EventTask'
        db.create_table(u'volunteer_eventtask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['volunteer.VolunteerTask'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['volunteer.Event'])),
        ))
        db.send_create_signal(u'volunteer', ['EventTask'])

        # Adding M2M table for field volunteers on 'EventTask'
        m2m_table_name = db.shorten_name(u'volunteer_eventtask_volunteers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('eventtask', models.ForeignKey(orm[u'volunteer.eventtask'], null=False)),
            ('volunteer', models.ForeignKey(orm[u'volunteer.volunteer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['eventtask_id', 'volunteer_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Timesheet', fields ['volunteer', 'day']
        db.delete_unique(u'volunteer_timesheet', ['volunteer_id', 'day'])

        # Deleting model 'VolunteerTask'
        db.delete_table(u'volunteer_volunteertask')

        # Deleting model 'Volunteer'
        db.delete_table(u'volunteer_volunteer')

        # Removing M2M table for field preferred_tasks on 'Volunteer'
        db.delete_table(db.shorten_name(u'volunteer_volunteer_preferred_tasks'))

        # Deleting model 'Timesheet'
        db.delete_table(u'volunteer_timesheet')

        # Deleting model 'TimesheetApproval'
        db.delete_table(u'volunteer_timesheetapproval')

        # Deleting model 'Event'
        db.delete_table(u'volunteer_event')

        # Deleting model 'EventTask'
        db.delete_table(u'volunteer_eventtask')

        # Removing M2M table for field volunteers on 'EventTask'
        db.delete_table(db.shorten_name(u'volunteer_eventtask_volunteers'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'volunteer.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'volunteer.eventtask': {
            'Meta': {'object_name': 'EventTask'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['volunteer.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['volunteer.VolunteerTask']"}),
            'volunteers': ('django.db.models.fields.related.ManyToManyField', [],
                           {'to': u"orm['volunteer.Volunteer']", 'symmetrical': 'False'})
        },
        u'volunteer.timesheet': {
            'Meta': {'unique_together': "(('volunteer', 'day'),)", 'object_name': 'Timesheet'},
            'day': ('django.db.models.fields.DateField', [], {}),
            'hours': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['volunteer.Volunteer']"})
        },
        u'volunteer.timesheetapproval': {
            'Meta': {'object_name': 'TimesheetApproval'},
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timesheet': ('django.db.models.fields.related.OneToOneField', [],
                          {'to': u"orm['volunteer.Timesheet']", 'unique': 'True'})
        },
        u'volunteer.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'United States'", 'max_length': '50'}),
            'emergency_contact': (
            'django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'emergency_contact_phone': (
            'django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'preferred_tasks': ('django.db.models.fields.related.ManyToManyField', [],
                                {'symmetrical': 'False', 'to': u"orm['volunteer.VolunteerTask']", 'null': 'True',
                                 'blank': 'True'}),
            'skills': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Volunteer'", 'max_length': '50'}),
            'user': (
            'django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'volunteer.volunteertask': {
            'Meta': {'object_name': 'VolunteerTask'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['volunteer']