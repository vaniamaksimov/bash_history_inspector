# bash_history_inspector
Задача:
Написать на python программу, которая бы с заданной периодичностью проверяла бы историю введенных
пользователем команд, читая bash history
 (https://www.cherryservers.com/blog/a-complete-guide-to-linux-bash-history)
 на наличие признаков ввода команд злоумышленником (примеры использования Linux-команд
 хакерами: https://gtfobins.github.io/). В случае обнаружения подозрительной команды должно быть
 отправлено сообщение по syslog с указанием: введенной команды.


1. Запускаем скрипт
2. Настраиваем HISTTIMEFORMAT echo 'HISTTIMEFORMAT="%d/%m/%y %T "' >> ~/.bashrc
3. Засыпаем на определенное пользователем время
4. Получаем логи из .bash_history
5. Проверяем логи