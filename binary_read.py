# hstFilename = "d:/Temp/EURUSD60.hst"
# file = 'C:\Users\Evgeniy\PycharmProjects\TICK\EURUSD43200.
import struct # Импортировали модуль для работы с двоичными записями.
file = 'EURUSD43200.hst'
# file = 'EURUSD1.hst'

hstf =  open(file, 'rb') #
ver, = struct.unpack("<i", hstf.read(4))  # Прочитали 4 байта из файла (номер версии формата данных).
print('Version: %d' % ver)  # Вывели на экран в форме целого числа. 400/401 старый/новый форматы

copywrite = hstf.read(64) # Строка копирайта (64 байта).
print('%s' % copywrite)
symbol = hstf.read(12) # Тикер (12 байт).
print('Symbol: %s' % symbol)
period,digits,timesign,last_sync  = struct.unpack("<iiii", hstf.read(16)) # Таймфрейм, число знаков, время создания, время синхронизации.
print('Timeframe: %d' % int(period))
print('Digits: %d' % int(digits))
import datetime # Для работы с датой и временем.
timesign_dt = datetime.datetime.fromtimestamp(timesign)
print('Timesign: ' + str(timesign_dt))
last_sync_dt = datetime.datetime.fromtimestamp(last_sync)
print('Last sync: ' + str(last_sync_dt))
unused = hstf.read(52) # Неиспользуемые данные в заголовке файла.

data = []  # Сюда будем записывать прочитанные данные.
count = 0  # Счётчик записей.
if ver == 400: # Если старый формат.
    len1 = 44  # Длина одной записи
    while len1 == 44:
        r1 = hstf.read(44) # Прочитали очередную запись из файла.
        len1 = len(r1)     # Длина прочитанной записи.
        if len1 == 44:     # Если прочитано 44 байта.
            ctm,open1,low1,high1,close1,vol1 = struct.unpack("<i5d", r1)
            dt = datetime.datetime.fromtimestamp(ctm)
            print('Date & Time: %d = %s %s' % (ctm, dt.date().strftime("%Y-%m-%d"), dt.time().strftime("%H:%M")))
            print('Open: %7.5f' % open1)
            print('Low %7.5f' % low1)
            print('High: %7.5f' % high1)
            print('Close %7.5f' % close1)
            print('Volume %d' % int(vol1))
            date1 = dt.date().strftime("%Y-%m-%d")
            time1 = dt.time().strftime("%H:%M")
            rw1 = [date1, time1, open1, high1, low1, close1, vol1]
            data.append(rw1) # Добавили прочитанные даные.
            print("----------------")
            count += 1       # Инкремент счётчика записей.
            if count > 5:    # После прочтения первых 5 записей
                hstf.close() # Закрываем файл.
                break        # Прерываем цикл.
elif ver == 401: # Если новый формат.
    len1 = 60    # Длина одной записи.
    while len1 == 60:
        r1 = hstf.read(60) # Прочитали очередную запись из файла.
        len1 = len(r1)     # Длина прочитанной записи.
        if len1 == 60:     # Если прочитано 60 байт.
            ctm,open1,low1,high1,close1,vol1,spread1,rvol1 = struct.unpack("<QddddQLQ", r1)
            dt = datetime.datetime.fromtimestamp(ctm)
            print('Date & Time: %d = %s %s' % (ctm, dt.date().strftime("%Y-%m-%d"), dt.time().strftime("%H:%M")))
            print('Open: %7.5f' % open1)
            print('Low %7.5f' % low1)
            print('High: %7.5f' % high1)
            print('Close %7.5f' % close1)
            print('Volume %d' % int(vol1))
            print('Spread %d' % spread1)
            print('Real volume %d' % int(rvol1))
            date1 = dt.date().strftime("%Y-%m-%d")
            time1 = dt.time().strftime("%H:%M")
            rw1 = [date1, time1, open1, high1, low1, close1, vol1, spread1, rvol1]
            data.append(rw1) # Добавили прочитанные даные.
            print("----------------")
            count += 1       # Инкремент счётчика записей.
            if count > 1000:    # После прочтения первых 5 записей
                hstf.close() # Закрываем файл.
                break        # Прерываем цикл.

print("Converted: %d bars" % count)
print(data)