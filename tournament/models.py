from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, date


# Create your models here.
class Tournament(models.Model):
    single = models.BooleanField('if the tournament is single', default=True)

    reg_end = models.DateTimeField('registration end time')
    draw_time = models.DateTimeField('draw time')

    start_date = models.DateField('start date')
    start_date_playoff = models.DateField('start date of play-off')
    end_date = models.DateField('end date')

    games_per_person = models.SmallIntegerField('number of games for each participant during the group stage', default=10)
    number_of_sets = models.SmallIntegerField('number of sets in one game of the group stage', default=5)
    game_start_time = models.TimeField('games start time', default="11:00:00")
    game_duration = models.DurationField('games duration', default="00:30:00")

    def __str__(self):
        return "{} - {}".format(date.strftime(self.start_date, '%d %B %Y'), date.strftime(self.end_date, '%d %B %Y'))

    def number_of_participants(self):
        return self.participant_set.count()


class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    email = models.EmailField('email', primary_key=True)
    first_name = models.CharField('first name', max_length=20)
    last_name = models.CharField('last name', max_length=20)
    drawn_number = models.SmallIntegerField('drawn number', blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.email == other.email
        return False

    def __ne__(self, other):
        return self.email != other.email

    def save(self, *args, **kwargs):
        if self.drawn_number is not None:
            games = self.tournament.game_set.all()
            for game in games:
                if game.id1 == self.drawn_number:
                    game.participant1 = self
                    game.save(first_call=False)
                if game.id2 == self.drawn_number:
                    game.participant2 = self
                    game.save(first_call=False)

        super(Participant, self).save(*args, **kwargs)

    def number_of_games(self):
        return self.participant1.count() + self.participant2.count()


class Game(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    id1 = models.SmallIntegerField('participant1 drawn number')
    id2 = models.SmallIntegerField('participant2 drawn number')
    participant1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant1', blank=True, null=True)
    participant2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant2', blank=True, null=True)
    game_date = models.DateField('game date', blank=True, null=True)
    start_time = models.TimeField('game start time', blank=True, null=True)

    def __str__(self):
        if self.participant1 and self.participant2:
            return "{} vs. {}".format(self.participant1, self.participant2)
        else:
            return "{} vs. {}".format(self.id1, self.id2)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.id1 == other.id1 and self.id2 == other.id2) or \
                   (self.id1 == other.id2 and self.id2 == other.id1)
        return False

    def __ne__(self, other):
        return (self.id1 != other.id1 or self.id2 != other.id2) and \
               (self.id1 != other.id2 or self.id2 != other.id1)

    def save(self, first_call=True, *args, **kwargs):
        if first_call:
            if self.id1 == self.id2:
                raise ValidationError("Participant1 and Participant2 are the same person", code=1)
            if self in self.tournament.game_set.all():
                raise ValidationError("Duplicate game : {}".format(self), code=2)
        super(Game, self).save(*args, **kwargs)


class SetResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    set_number = models.SmallIntegerField('set number')
    result1 = models.SmallIntegerField('participant1 result')
    result2 = models.SmallIntegerField('participant2 result')

    def __str__(self):
        return "{} {} set result".format(self.game, self.set_number)
