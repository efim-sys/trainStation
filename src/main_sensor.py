from machine import Pin, ADC, PWM
from time import sleep
import machine
import ubinascii
from micropyserver import MicroPyServer
import network

led = Pin(15, Pin.OUT)

delta = 1  # Переменная для указания типа работы датчика (вход/выход)
counter = 0  # Счетчик людей в помещении

led.off()

adc = ADC(Pin(7))
adc.atten(ADC.ATTN_11DB)  # подключение АЦП для определения заряда батареи

led.off()

wlan = network.WLAN(network.STA_AP)
wlan.active(True)
wlan.config(essid="MicroSanitizer", password="cL*b931aLTV~vq$h") # Создание точки доступа Wi-Fi

while not wlan.active(): pass

print("Start...")
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("MAC: " + mac)
print("Connected... IP: " + wlan.ifconfig()[0])   
    
f = open("index.html", 'r')  # Получение файла с веб-страницей из файловой системы
index = f.read()
f.close()
    
def do_index(request):   # Отправка веб-страницы клиенту
    voltage = round(adc.read_uv()/500000, 3)
    server.send(index % (mac, str(voltage), (voltage-3)/0.0125))
    
def send_people(request):  # Отправка количества людей в помещении
    global counter
    server.send(str(counter))
    
def ch_type(request):  # Страница для смены типа датчика (на вход или на выход)
    global delta
    delta *= -1
    server.send("<a href='/'>Go back</a>")
    
def do_drop(request):  # Сброс значений датчика в 0 (Для отладки)
    global counter
    counter = 0
    server.send("<a href='/'>Go back</a>")

server = MicroPyServer()  # создание веб-сервера и всех веб-страниц
server.add_route("/", do_index)
server.add_route("/people", send_people)
server.add_route("/type", ch_type)
server.add_route("/drop", do_drop)

PWM(led).duty(100)  # Светодиод на плате оповещает о работе тусклым светом

def inc_counter(pp):  # Функция увеличения счетчика людей в прерывании
    global counter
    counter+=delta
    print("Обнаружен человек! В здании %d штук."%counter)

sensor = Pin(3, Pin.IN)
sensor.irq(inc_counter, Pin.IRQ_RISING)  # Создание прерывания по выходу с датчика

server.start()  # Основной цикл веб-сервера

