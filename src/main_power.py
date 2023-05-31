from machine import Pin, PWM
from time import sleep
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("MicroSanitizer", "cL*b931aLTV~vq$h")  # Подключение к точке доступа
while not wlan.isconnected(): pass

maxPeople = 2000 # Значение кол-ва посетителей вокзала при макс. загрузке

pwm = PWM(Pin(15, Pin.OUT))  # Объект для управления мощностью лампы

def http_get(url):  # Функция для отправки GET - запроса
    try:
        import socket
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                return str(data, 'utf8')
            else:
                break
        s.close()
    except:
        return str(maxPeople)  # При невозможности подключения к датчику установится макс. значение лудей в здании

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

while True:
    people = constrain(int(http_get("http://192.168.1.53/people")), 0, maxPeople)  # Получение кол-ва людей в здании
    power = 123+900*(people+1)/maxPeople  # Вычисление необходимой мощности лампы (0-1023)
    print(people, power)
    pwm.duty(int(power)) # Установка мощности
    sleep(2)  # Мощность обновляестя раз в 2 секунды