import config
import telebot
from ics import Calendar, Event
c = Calendar()
e = Event()
e.name = "My cool event"
e.begin = '2014-01-01 00:00:00'
c.events.add(e)
c.events
# {<Event 'My cool event' begin:2014-01-01 00:00:00 end:2014-01-01 00:00:01>}
with open('/Users/andreezy/calendar/my.ics', 'w') as f:
    f.write(str(c))
bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def start(message):
    # sendDocument
    doc = open('/Users/andreezy/calendar/my.ics', 'rb')
    bot.send_document(184022333, doc)




bot.polling(none_stop=True)

# And it's done !

# iCalendar-formatted data is also available in a string

# 'BEGIN:VCALENDAR\nPRODID:...