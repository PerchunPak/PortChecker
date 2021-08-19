from mcstatus import MinecraftServer
from socket import socket, AF_INET, SOCK_STREAM
from time import time

IP = '1.1.1.1' # айпи который пинговать, можно и домен
port = 0 # порт с которого начинать брут
ports_long = 0
sum_ports = 0
sum_ports_all = 0
TIME_PERIOD_FOR_PORT_CHECKING = 0.02
with open("results.txt", "a") as log:
    while int(port) <= 25600:
        server = MinecraftServer.lookup(IP + ':' + str(port))
        try:
            status = server.status()
            online = True
        except OSError:
            online = False
        if online:
            print('Сервер найден, порт: %s' % port)
            log.write('Сервер %s\n' % port)
            port += 1
        else:
            print('Порт %s не рабочий' % port)

            start_time = time()
            sock = socket(AF_INET, SOCK_STREAM)
            result = sock.connect_ex((IP, int(port)))
            if result != 0:
                log.write('Открытый %s\n' % port)
                print('Найден открытый порт %s' % port)
                log.write('Закрытый %s \n' % port)
                print('Найден закрытый порт %s' % port)
            end_time = time() - start_time
            print('Закончило проверку порта %s за %s' % (port, str(end_time)))

            if end_time >= TIME_PERIOD_FOR_PORT_CHECKING:
                ports_long = ports_long + 1
                print('Что то слушает на порту %s' % port)
                log.write('Слушает %s\n' % port)
            else:
                sum_ports += end_time

            sum_ports_all += end_time

            sock.close()

            port += 1
    print('Средний пинг ' + str((sum_ports_all / port)))
    print('Средний пинг (без длинных ответов) ' + str((sum_ports / (port - ports_long))))
print('Конец')
