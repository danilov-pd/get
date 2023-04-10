# Написать скрипт, который реализует АЦП при помощи последовательного перебора значений
# создать скрипт 5-1-adc-simple.py
# в созданном скрипте импортировать модуль работы с GPIO на Raspberry Pi
import RPi.GPIO as GPIO
import time

# объявить переменную dac - список указанных на плате номеров GPIO-пинов в области DAC
dac = [10, 9, 11, 5, 6, 13, 19, 26]
len_dac = len(dac)
leds = [21, 20, 16, 12, 7, 8, 25, 24]
leds.reverse()
len_leds = len(leds)
# объявить переменную comp - c номером GPIO-пина, указанного на плате в секции COMP
comp = 4
# объявить переменную troyka - c номером GPIO-пина, указанного на плате в секции TROYKA MODULE
troyka = 17
# настроить режим обращения к GPIO
GPIO.setmode(GPIO.BCM)
# одной строкой кода настроить на выход все 8 GPIO-пинов из списка dac
GPIO.setup(dac, GPIO.OUT)
# настроить на выход GPIO-пин тройка-модуля и задать значение по умолчанию при помощи аргумента initial в функции GPIO.setup
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
# настроить на вход GPIO-пин comp
GPIO.setup(comp, GPIO.IN)

# добавить функцию перевода десятичного числа в список 0 и 1 из прошлого занятия
def dec2bin(dec, bits):
    binary = [0] * bits
    for i in range(bits):
        binary[i] = (dec >> i) % 2
    return binary

def adc_1():
    # в функции должен выполнятся последовательный перебор значений и установка их на dac и считывание значения с comp
    GPIO.output(dac, 0)
    time.sleep(0.005)
    for i in range(256):
        out = dec2bin(i, len_dac)
        GPIO.output(dac, out)
        inp = GPIO.input(comp)
        if inp == 0:
            return i
        time.sleep(0.005)
    return 0


# описать функцию adc(), которая возвращает десятичное число, пропорциональное напряжению клемме S тройка-модуля
def adc_2():
    # в функции adc() реализовать алгоритм последовательного приближения, 
    # описанный в видео **"5-3 - АЦП - Последовательный АЦП"**
    voltage = 0
    for i in range(7, -1, -1):
        voltage += 2 ** i
        GPIO.output(dac, dec2bin(voltage, len_dac))
        time.sleep(0.01)
        if GPIO.input(comp) == 0:
            voltage -= 2 ** i
    return voltage

def set_leds(value, n_leds):
    values = [0] * n_leds
    to_light = round((value / 0.828) * n_leds)
    to_light = min(n_leds, to_light)
    for i in range(to_light):
        values[i] = 1
    return values

# добавить в скрипт два блока: try и finally
# в блоке try:
try:
    # в бесконечном цикле вызывать функцию adc()
    while True:
        time.sleep(0.5)
        voltage = adc_1() * 3.3 / 255
        GPIO.output(leds, set_leds(voltage, len_leds))
        print('Method 1: {:.3f} V, leds: '.format(voltage ), set_leds(voltage, len_leds))
        time.sleep(0.5)
        voltage = adc_2() * 3.3 / 255
        GPIO.output(leds, set_leds(voltage, len_leds))
        print('Method 2: {:.3f} V, leds:'.format(voltage), set_leds(voltage, len_leds))

# в блоке finally подать 0 на все использовавшиеся выходные пины и очистить настройки GPIO
finally:
    GPIO.output(leds, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()
# возвращаемое значение функции переводить в напряжение
# на экран выводить цифровое значение и соответствующее ему значение напряжения
# При запуске скрипта для установления напряжения на SIG воспользоваться потенциометром. Проверить напряжение на клемме S при помощи мультиметра и сравнить с выведенным на экран

