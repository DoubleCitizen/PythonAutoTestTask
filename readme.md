**Описание работы программы с примерами вывода и инструкции по запуску**

Команда запускает тестирование доступности сервера по http, следующих ссылок:

-H http://ya.ru, https://google.com, https://youtube.com

-C 5 количество запросов
```
python bench.py -H "http://ya.ru,https://google.com,https://youtube.com" -C 5
```
Команда запускает тестирование доступности сервера по http, следующих ссылок:

-H http://ya.ru,https://google.com,https://youtube.com

-C 2 количество запросов

-O text.txt

```
python bench.py -H "http://ya.ru,https://google.com,https://youtube.com" -C 2 -O text.txt
```
Команда запускает тестирование доступности сервера по http, следующих ссылок:

-C 2 количество запросов

-O text.txt

-F hosts.txt

```
python bench.py -C 2 -O text.txt -F hosts.txt
```

Команда вызовет ошибку:
usage: bench.py [-h] [-H HOSTS] [-C COUNT] [-F FILE] [-O OUTPUT]
bench.py: error: Specify only one of -H/--hosts or -F/--file.

```
python bench.py -H "http://ya.ru,https://google.com,https://youtube.com" -C 2 -O text.txt -F hosts.txt
```

Файл hosts.txt должен выглядить примерно так:
```txt
http://ya.ru
https://google.com
https://youtube.com
```

Команды и их описание:
```
–H/--hosts  # тип str Список хостов, разделенных запятыми, для тестирования
–C/--count  # тип int Количество запросов для отправки каждому хосту
-F/--file   # тип Path Файл, из которого будут считаны хосты для тестирования
-O/--output # тип Path Запись выходной информации в файл
# Примечание нельзя использовать параметры –H/--hosts и -F/--file одновременно
# а также обязателен хотя бы один параметр из –H/--hosts и -F/--file
```

При указании выходного файла (output.txt), данные в файл дописываются и выглядят примерно следующим образом:
```
Statistics for host: https://youtube.com
Success: 0
Failed: 0
Errors: 2
Min time: 0.0000 seconds
Max time: 0.0000 seconds
Avg time: 0.0000 secondsStatistics for host: http://ya.ru
Success: 2
Failed: 0
Errors: 0
Min time: 0.1726 seconds
Max time: 0.4500 seconds
Avg time: 0.3113 seconds
Statistics for host: https://google.com
Success: 2
Failed: 0
Errors: 0
Min time: 0.3601 seconds
Max time: 0.3664 seconds
Avg time: 0.3633 seconds
Statistics for host: https://youtube.com
Success: 0
Failed: 0
Errors: 2
Min time: 0.0000 seconds
Max time: 0.0000 seconds
Avg time: 0.0000 seconds
```