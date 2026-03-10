from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zettrack_app', '0008_notificationsetting_notification_announcement'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicHoliday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='public_holidays', to='zettrack_app.company')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
