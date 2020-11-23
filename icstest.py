# # import config
# # import telebot
# # from ics import Calendar, Event
# # c = Calendar()
# # e = Event()
# # e.name = "My cool event"
# # e.begin = '2014-01-01 00:00:00'
# # c.events.add(e)
# # c.events
# # # {<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>}
# # with open('/Users/andreezy/calendar/my.ics', 'w') as f:
# #     f.write(str(c))
# # bot = telebot.TeleBot(config.token)
# #
# # @bot.message_handler(content_types=["text"])
# # def start(message):
# #     # sendDocument
# #     doc = open('/Users/andreezy/calendar/my.ics', 'rb')
# #     bot.send_document(184022333, doc)
# #
# #
# #
# #
#
# #
# # # And it's done !
# #
# # # iCalendar-formatted data is also available in a string
# #
# # # 'BEGIN:VCALENDAR\nPRODID:...
# from __future__ import print_function
#
# import config
# import telebot
#
#
#
# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# bot = telebot.TeleBot(config.token)
# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#
#
# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials2.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
#     service = build('calendar', 'v3', credentials=creds)
#
#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])
#
#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])
#
#
# @bot.message_handler(content_types=["text"])
# def start(message):
#     # sendDocument
#     main()
#
#
#
# if __name__ == '__main__':
#     bot.polling(none_stop=True)
#
#
#
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# scopes = ['https://www.googleapis.com/auth/calendar']
# flow = InstalledAppFlow.run_console()
# credentials = flow.run_console()
# import pickle
# pickle.dump(credentials, open("token.pkl", "wb"))
# credentials = pickle.load(open("token.pkl", "rb"))
# service = build("calendar", "v3", credentials=credentials)