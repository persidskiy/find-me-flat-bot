import gevent
import urllib2
import urllib
import json
import os
from gevent.monkey import patch_all
from cian import parse
from utils import log, save_json, load_json

patch_all()

CHATS_FILE = "chats.json"
KNOWN_FILE = "known.json"

messages_queue = []
data_dir = os.path.join(os.path.dirname(__file__), "data")
chats_path = os.path.join(data_dir, CHATS_FILE)
known_path = os.path.join(data_dir, KNOWN_FILE)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

chats = load_json(chats_path, {})

def add_chat(chat_id, url):
    chats[chat_id] = url
    save_json(chats_path, chats)
    log("Added chat {}: {}".format(chat_id, url))


def remove_chat(chat_id):
    del chats[chat_id]
    save_json(chats_path, chats)
    log("Chat {}: Removed from queue".format(str(chat_id)))


def load_telegram_method(method, params):
    unicode_params = {}
    for k, v in params.iteritems():
        val = v.encode("utf8") if isinstance(v, unicode) else v
        unicode_params[k] = val

    params_str = urllib.urlencode(unicode_params)
    token = os.environ["TG_BOT_TOKEN"]
    url = u"https://api.telegram.org/bot{}/{}?{}".format(token,
                                                         method,
                                                         params_str)
    return json.load(urllib2.urlopen(url), encoding="utf-8")


def request_updates(offset):
    params = {u"offset": offset,
              u"timeout": 60}
    return load_telegram_method("getUpdates", params)


def send_message(chat_id, message):
    params = {u"chat_id": chat_id,
              u"text": message}
    return load_telegram_method("sendMessage", params)


def updater():
    log("Bot started")
    offset = 0
    while True:
        updates_response = request_updates(offset)
        try:
            updates = updates_response.get("result", [])
        except urllib2.HTTPError, e:
            gevent.sleep(10)
            continue

        if len(updates) > 0:
            offset = updates[-1].get("update_id", offset) + 1
            message_updates = filter(
                lambda u: "message" in u and "text" in u["message"],
                updates)
            for upd in message_updates:
                text = upd["message"]["text"]
                chat_id = str(upd["message"]["chat"]["id"])
                log("Got message (chat:{}): {}".format(chat_id, text))
                handle_message(chat_id, text)


def handle_message(chat_id, message):
    if message.find(u"/start") == 0:
        parts = message.split(u" ")
        if len(parts) == 2:
            add_chat(chat_id, parts[1])
            send_message(chat_id, "Ok, you will receive messages")
        else:
            send_message(chat_id, "Usage: /start <cian_url>")   
    elif message == u"/stop":
        remove_chat(chat_id)
        send_message(chat_id, "Ok, you will not receive messages")
    if message == u"/ping":
        log("ping  {}".format(json.dumps(chats)))
        send_message(chat_id,
                     u"Pong! Subscribed: {}".format(chats.get(chat_id, False)))


def parser():
    while True:
        log("Parse for chats: {}".format(json.dumps(chats)))
        chats_copy = chats.copy()
        for chat_id, url in chats_copy.iteritems():
            log("Parse {} : {}".format(chat_id, url))
            refs = parse(known_path, url)
            log("Parsed {}".format(len(refs), url))
            if len(refs) > 0:
                message = u"\n".join(refs)
                send_message(chat_id, message)
        sleep_time = 10 if len(chats_copy) == 0 else 600
        log("Sleep: {}ms".format(sleep_time))
        gevent.sleep(sleep_time)


def main():
    gevent.joinall([
        gevent.spawn(updater),
        gevent.spawn(parser),
    ])


if __name__ == "__main__":
    main()
