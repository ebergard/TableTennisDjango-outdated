# Generated by Django 2.1.7 on 2019-05-09 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1', models.SmallIntegerField(verbose_name='Participant1 drawn number')),
                ('id2', models.SmallIntegerField(verbose_name='Participant2 drawn number')),
                ('game_date', models.DateField(blank=True, null=True, verbose_name='Game date')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='Game start time')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, verbose_name='Email')),
                ('first_name', models.CharField(max_length=20, verbose_name='First name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last name')),
                ('drawn_number', models.SmallIntegerField(blank=True, null=True, verbose_name='Drawn number')),
            ],
        ),
        migrations.CreateModel(
            name='SetResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_number', models.SmallIntegerField(verbose_name='Set number')),
                ('result1', models.SmallIntegerField(verbose_name='Participant1 result')),
                ('result2', models.SmallIntegerField(verbose_name='Participant2 result')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('single', models.BooleanField(default=True, verbose_name='if the tournament is single')),
                ('reg_end', models.DateTimeField(verbose_name='registration end time')),
                ('draw_time', models.DateTimeField(verbose_name='draw time')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('start_date_playoff', models.DateField(verbose_name='start date of play-off')),
                ('end_date', models.DateField(verbose_name='end date')),
                ('games_per_person', models.SmallIntegerField(default=10, verbose_name='number of games for each participant during the group stage')),
                ('number_of_sets', models.SmallIntegerField(default=5, verbose_name='number of sets in one game of the group stage')),
                ('game_start_time', models.TimeField(default='11:00:00', verbose_name='games start time')),
                ('game_duration', models.DurationField(default='00:30:00', verbose_name='games duration')),
            ],
        ),
        migrations.AddField(
            model_name='participant',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='game',
            name='participant1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant1', to='tournament.Participant'),
        ),
        migrations.AddField(
            model_name='game',
            name='participant2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant2', to='tournament.Participant'),
        ),
        migrations.AddField(
            model_name='game',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Tournament'),
        ),
    ]
