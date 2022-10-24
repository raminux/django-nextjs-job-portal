# Generated by Django 4.1.2 on 2022-10-23 01:09

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jobs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('job_type', models.CharField(choices=[('Permanent', 'Permanent'), ('Temporary', 'Temporary'), ('Internship', 'Internship')], default='Permanent', max_length=30)),
                ('education', models.CharField(choices=[('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('Phd', 'Phd')], default='Bachelors', max_length=30)),
                ('industry', models.CharField(choices=[('Business', 'Business'), ('Information Technology', 'It'), ('Banking', 'Banking'), ('Education/Training', 'Education'), ('Telecommunication', 'Telecommunication'), ('Others', 'Others')], default='Business', max_length=30)),
                ('experience', models.CharField(choices=[('NO_EXPERIENCE', 'No Experience'), ('1 Year', 'One Year'), ('2 Years', 'Two Years'), ('3 Years above', 'Three Years Plus')], default='NO_EXPERIENCE', max_length=30)),
                ('salary', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)])),
                ('positions', models.IntegerField(default=1)),
                ('company', models.CharField(max_length=100, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0.0, 0.0), srid=4326)),
                ('last_apply_date', models.DateTimeField(default=jobs.models.return_date_time)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]