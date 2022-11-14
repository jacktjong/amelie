# Generated by Django 2.2.25 on 2022-05-30 18:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


def copy_courses_to_backup_courses(apps, schema_editor):
    Course = apps.get_model('education', 'Course')
    BackupCourse = apps.get_model('education', 'BackupCourse')
    for course in Course.objects.all():
        bc = BackupCourse.objects.create(name=course.name, course_code=course.course_code, id=course.id,
                                         course_type=course.course_type)


def move_courses_to_basecourse(apps, schema_editor):
    BackupCourse = apps.get_model('education', 'BackupCourse')
    Course = apps.get_model('education', 'Course')
    Module = apps.get_model('education', 'Module')
    for course in BackupCourse.objects.all():
        if course.course_type == 'MOD':
            Module.objects.create(name=course.name, course_code=course.course_code, id=course.id)
        else:
            Course.objects.create(name=course.name, course_code=course.course_code, id=course.id)


def move_old_course_to_course_complaint(apps, schema_editor):
    Complaint = apps.get_model('education', 'Complaint')
    Course = apps.get_model('education', 'Course')
    Module = apps.get_model('education', 'Module')
    for complaint in Complaint.objects.all():
        if complaint.old_course is None:
            continue
        try:
            fk = Course.objects.get(id=complaint.old_course.pk)
            complaint.course = Course.objects.get(pk=fk)
        except Course.DoesNotExist:
            fk = Module.objects.get(id=complaint.old_course.pk)
            complaint.course = Module.objects.get(pk=fk)
        complaint.save()


class Migration(migrations.Migration):
    dependencies = [
        ('education', '0003_complaintcomment_official_squashed_0006_auto_20211211_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackupCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('course_type',
                 models.CharField(choices=[('MOD', 'Module'), ('COURSE', 'Course')], default='COURSE',
                                  max_length=6, verbose_name='Course type')),
                ('course_code', models.PositiveIntegerField(unique=True, validators=[
                    django.core.validators.MinValueValidator(100000),
                    django.core.validators.MaxValueValidator(999999999)], verbose_name='Course code')),
            ],
            options={
                'verbose_name': 'Course',
                'ordering': ['name', 'course_code'],
                'verbose_name_plural': 'Courses',
            },
        ),
        migrations.RunPython(
            copy_courses_to_backup_courses,
        ),
        migrations.AlterField(
            model_name='complaint',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='education.BackupCourse', verbose_name='BackupCourse')
        ),
        migrations.DeleteModel(
            name='course',
        ),
        migrations.CreateModel(
            name='BaseCourseModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('course_code', models.PositiveIntegerField(unique=True, validators=[
                    django.core.validators.MinValueValidator(100000),
                    django.core.validators.MaxValueValidator(999999999)], verbose_name='Course code')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('basecoursemodule_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='education.BaseCourseModule')),
            ],
            options={
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
                'ordering': ['name', 'course_code'],
            },
            bases=('education.basecoursemodule',),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('basecoursemodule_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='education.BaseCourseModule')),
                ('module_ptr',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='courses',
                                   to='education.Module', blank=True, verbose_name='Module')),
            ],
            options={
                'verbose_name': 'Course',
                'ordering': ['name', 'course_code'],
                'verbose_name_plural': 'Courses',
            },
            bases=('education.basecoursemodule',),
        ),
        migrations.RunPython(
            move_courses_to_basecourse,
        ),
        migrations.RenameField(
            model_name='complaint',
            old_name='course',
            new_name='old_course',
        ),
        migrations.AddField(
            model_name='complaint',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='education.BaseCourseModule', verbose_name='Course or module'),
        ),
        migrations.RunPython(
            move_old_course_to_course_complaint,
        ),
        migrations.RemoveField(
            model_name='complaintcomment',
            name='official',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='old_course'
        ),
        migrations.DeleteModel(
            name='BackupCourse'
        )
    ]
