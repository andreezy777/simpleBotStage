# # # import config
# # # import telebot
# # # from ics import Calendar, Event
# # # c = Calendar()
# # # e = Event()
# # # e.name = "My cool event"
# # # e.begin = '2014-01-01 00:00:00'
# # # c.events.add(e)
# # # c.events
# # # # {<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>}
# # # with open('/Users/andreezy/calendar/my.ics', 'w') as f:
# # #     f.write(str(c))
# # # bot = telebot.TeleBot(config.token)
# # #
# # # @bot.message_handler(content_types=["text"])
# # # def start(message):
# # #     # sendDocument
# # #     doc = open('/Users/andreezy/calendar/my.ics', 'rb')
# # #     bot.send_document(184022333, doc)
# # #
# # #
# # #
# # #
# #
# # #
# # # # And it's done !
# # #
# # # # iCalendar-formatted data is also available in a string
# # #
# # # # 'BEGIN:VCALENDAR\nPRODID:...
# # from __future__ import print_function
# #
# # import config
# # import telebot
# #
# #
# import config
# import telebot
# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# import logging
# import cherrypy
# bot = telebot.TeleBot(config.token)
#
#
#
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
#
# bot = telebot.TeleBot(config.token)
# day = ''
# day_delete = ''
#
#
# WEBHOOK_HOST = 'scheduler.hmainnetwork.keenetic.pro'
# WEBHOOK_PORT = 8443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
# WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше
#
# WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу
#
# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % (config.token)
#
#
#
# class WebhookServer(object):
#     @cherrypy.expose
#     def index(self):
#         if 'content-length' in cherrypy.request.headers and \
#                         'content-type' in cherrypy.request.headers and \
#                         cherrypy.request.headers['content-type'] == 'application/json':
#             length = int(cherrypy.request.headers['content-length'])
#             json_string = cherrypy.request.body.read(length).decode("utf-8")
#             update = telebot.types.Update.de_json(json_string)
#             # Эта функция обеспечивает проверку входящего сообщения
#             bot.process_new_updates([update])
#             return ''
#         else:
#             raise cherrypy.HTTPError(403)
#
#
#
# # If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#
#
#
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
# creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
# if os.path.exists('token.pickle'):
#     with open('token.pickle', 'rb') as token:
#         creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#         creds = flow.run_local_server(port=80)
#         # Save the credentials for the next run
#     with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#
# service = build('calendar', 'v3', credentials=creds)
#
#     # Call the Calendar API
# now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
# print('Getting the upcoming 10 events')
# events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
# events = events_result.get('items', [])
#
# if not events:
#     print('No upcoming events found.')
# for event in events:
#     start = event['start'].get('dateTime', event['start'].get('date'))
# print(start, event['summary'])
#
#
# @bot.message_handler(content_types=["text"])
# def start(message):
#     # sendDocument
#     bot.reply_to(msg,"привет")
#
#
#
# if __name__ == '__main__':
#     bot.remove_webhook()
#
#     # Ставим заново вебхук
#     bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                     certificate=open(WEBHOOK_SSL_CERT, 'r'))
#
#     cherrypy.config.update({
#         'server.socket_host': WEBHOOK_LISTEN,
#         'server.socket_port': WEBHOOK_PORT,
#         'server.ssl_module': 'builtin',
#         'server.ssl_certificate': WEBHOOK_SSL_CERT,
#         'server.ssl_private_key': WEBHOOK_SSL_PRIV
#     })
#
#     # Собственно, запуск!
#     cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
# #
# #
# #
# # from googleapiclient.discovery import build
# # from google_auth_oauthlib.flow import InstalledAppFlow
# # scopes = ['https://www.googleapis.com/auth/calendar']
# # flow = InstalledAppFlow.run_console()
# # credentials = flow.run_console()
# # import pickle
# # pickle.dump(credentials, open("token.pkl", "wb"))
# # credentials = pickle.load(open("token.pkl", "rb"))
# # service = build("calendar", "v3", credentials=credentials)






import os
import pprint

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

pp = pprint.PrettyPrinter(indent=2)

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "credentials.json"

# This access scope grants read-only access to the authenticated user's Drive
# account.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def list_drive_files(service, **kwargs):
  results = service.files().list(
    **kwargs
  ).execute()

  pp.pprint(results)

if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  service = get_authenticated_service()
  list_drive_files(service,
                   orderBy='modifiedByMeTime desc',
                   pageSize=5)