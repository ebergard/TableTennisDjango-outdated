# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import Tournament, Participant, SetResult, Game
from .forms import RegisterForm, ResultForm
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from tournament.functions import generate_games, generate_schedule, get_current_tournament, get_tournament_status


def index(request):
    status_msg = {
        0: "Открыта регистрация на турнир",
        1: "Регистрация на турнир завершена",
        2: "Идёт турнир...",
        3: "Турнир завершён.",
        4: "Нет данных о турнирах",
    }
    tournament = get_current_tournament()
    tournament_status = get_tournament_status(tournament)
    msg = status_msg[tournament_status]
    return render(request, 'tournament/index.html', locals())


def register(request):
    tournament = get_current_tournament()
    tournament_status = get_tournament_status(tournament)
    if tournament_status == 0:
        register_open = True
        msg = "Регистрация на турнир:"
    else:
        register_open = False
        msg = "Открытых регистраций нет"

    if register_open:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                p = Participant(tournament=tournament,
                                first_name=form.cleaned_data['first_name'],
                                last_name=form.cleaned_data['last_name'],
                                email=form.cleaned_data['email'])
                try:
                    p.save()
                except IntegrityError:
                    return HttpResponseRedirect('/failure')
                return HttpResponseRedirect('/success')
        else:
            form = RegisterForm()

    return render(request, 'tournament/register.html', locals())


def success(request):
    success = True
    tournament = get_current_tournament()
    tournament_status = get_tournament_status(tournament)
    return render(request, 'tournament/register_result.html', locals())


def failure(request):
    success = False
    tournament = get_current_tournament()
    tournament_status = get_tournament_status(tournament)
    return render(request, 'tournament/register_result.html', locals())


def participants(request):
    tournament = get_current_tournament()
    tournament_status = get_tournament_status(tournament)
    if tournament_status in (0, 1, 2):
        return render(request, 'tournament/participants.html', locals())
    else:
        return HttpResponse("<h2>Participants list is not available</h2>")


def rating(request):
    tournament = get_current_tournament()
    for p in tournament.participant_set.all():
        p.win_sets = 0
        p.win_balls = 0
        p.games_left = 0
        for g in Game.objects.filter(Q(participant1=p) | Q(participant2=p)):
            if g.setresult_set.exists():
                for r in g.setresult_set.all():
                    if g.participant1 == p:
                        if r.result1 > r.result2:
                            p.win_sets += 1
                        p.win_balls += r.result1 - r.result2
                    else:
                        if r.result2 > r.result1:
                            p.win_sets += 1
                        p.win_balls += r.result2 - r.result1
            else:
                p.games_left += 1
        p.save()

    participants = list(tournament.participant_set.all())
    participants.sort(key=lambda elem: (elem.win_sets, elem.win_balls), reverse=True)

    tournament_status = get_tournament_status(tournament)
    if tournament_status in (0, 1, 2):
        return render(request, 'tournament/rating.html', locals())
    else:
        return HttpResponse("<h2>Participants rating is not available</h2>")


def games(request, game=None):
    tournament = get_current_tournament()
    tournament_status = get_tournament_status(tournament)
    games = tournament.game_set.all().order_by('game_date', 'start_time')

    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            game = Game.objects.get(pk=game)
            for i in range(1, 6):
                p = SetResult(game=game,
                              set_number=i,
                              result1=form.cleaned_data['set{}res1'.format(i)],
                              result2=form.cleaned_data['set{}res2'.format(i)])
                try:
                    p.save()
                except IntegrityError:
                    return HttpResponseRedirect('/failure')
            return HttpResponseRedirect('/games')
    else:
        form = ResultForm()

    if tournament_status in (0, 1, 2):
        return render(request, 'tournament/games.html', locals())
    else:
        return HttpResponse("<h2>Games list is not available</h2>")


def before_draw(request):
    # Generate new schedule
    games = generate_games()
    generate_schedule(games)
    return HttpResponse("Schedule generated")
