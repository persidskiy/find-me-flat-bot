find-me-flat-bot
================

Ботик для telegram, который будет мониторить cian и скидывать вам новые объявления в Telegram.

Как настроить:
1. Заводим своего бота в телеграме, [@BotFather](https://t.me/BotFather) вам в помощь. Главное - получить токен.
2. В любом облаке заводим инстанс с Docker. Это можно сделать за пару кликов в [DigitalOcean](https://m.do.co/c/f099e32edcfe).
3. Дальше все просто:

```bash
git clone git@github.com:persidskiy/find-me-flat-bot.git
cd find-me-flat-bot
docker build . -t "find-me-flat-bot"

# в обычном режиме:
docker run -t -e TG_BOT_TOKEN="<token>" find-me-flat-bot:latest
# в режиме демона
docker run -d -e TG_BOT_TOKEN="<token>" find-me-flat-bot:latest
```

Ваш бот готов, можно написать ему `/ping`, он должен ответить.

Команды
-------

```
/start <url> - Начать наблюдать за объявлениями по этому url
/stop - Закончить наблюдение
/ping - Проверить, что бот жив. За одно он вернет текущий наблюдаемый URL.
```

URL для парсинга - URL страницы на Cian со всеми примененными фильтрами и отображением в виде списка (это важно) 
[пример](https://www.cian.ru/cat.php?currency=2&deal_type=rent&district%5B0%5D=21&engine_version=2&maxprice=60000&offer_type=flat&room1=1&room2=1&totime=-2&type=4&wp=1)


