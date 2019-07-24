# -*- coding: utf-8 -*-
# Run this script from APPLIEDTECH domain
# to send an email with a text to the participants

from functions import *

messages = {
    "Взнос за участие в турнире": "Всем привет,\n\nесли вы ещё не сдали деньги за участие в турнире, просьба сделать"
                                  " это в ближайшее время (голубой сектор, место В15).\n\nСпасибо.\n\n",
    "Жеребьёвка": "Всем привет,\n\nесли вы хотите сами вытянуть свой номер на жеребьёвке, подходите к теннисной сегодня"
                  " к 15:00 (не обязательно).\n\n"
}

if SINGLE:
    sheetname = "личное первенство"
else:
    sheetname = "парный турнир"


emails = gather_emails(NUMBER_OF_PARTICIPANTS, sheetname)
send_email_to_all(emails, "Взнос за участие в турнире", messages["Взнос за участие в турнире"])
