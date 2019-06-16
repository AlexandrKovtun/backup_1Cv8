from datetime import datetime
from os import remove, system, path
import zipfile
from clint.textui import colored # модуль для печати разными цветами
from time import gmtime, strftime
from shutil import copyfileobj, make_archive

today = datetime.today()

system("mode con cols=65 lines=17") # задаём размер окна консоли
print("")
print("           РЕЗЕРВНОЕ КОПИРОВАНИЕ ФАЙЛА БАЗЫ 1Cv8.1CD")
print(" =============================================================== ")

# конвертирует байты в Кб, Мб, Гб и Тб
def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

filename1 = "1Cv8.1CD"

try: 										# проверяем, есть ли файл базы в папке
    file1 = open(filename1,"rb")
except IOError: 							# если нет, то выкинуть исключение
    print (colored.red ("\n ОШИБКА!") )
    print(" Файла базы (1Cv8.1CD) нет в этой папке!\n Поместите программу в папку с базой...")
else:
	filename2 = input(' Введите префикс бэкапа или нажмите "ENTER":\n ')
	# если юзер не ввёл префикс, тогда префикс будет "backup_"
	if filename2 == "":
		filename2 = "backup_" + today.strftime("%d.%m.%Y_%H.%M") + "_" + filename1
	else:
		filename2 = filename2 + "_" + today.strftime("%d.%m.%Y_%H.%M") + "_" + filename1
	s = datetime.today() # время начала операции

	file2 = open(filename2,"wb") # открываем файл-приёмник в режиме перезаписи
	print(" Копирование начато! Ожидайте...")
	copyfileobj(file1, file2, 1024*1024) # копирование (имя1, имя2, размер буфера при копировании)
	file1.close()
	file2.close()	  # закрываем файлы
	
	print(" Копирование успешно завершено!")
	print(" Был создан файл ", filename2)
	print("")

	# упаковываем в архив созданную копию файла
	print(" Начата упаковка файла в zip-архив! Ожидайте...")
	zip_name = filename2 + ".zip"
	my_zip = zipfile.ZipFile(zip_name, mode='w', allowZip64=True)
	my_zip.write(filename2, compress_type=zipfile.ZIP_DEFLATED)
	my_zip.close()

	remove(filename2) # удаляем созданную копию файла

	size = path.getsize(zip_name) # получаем размер файла архива
	e = datetime.today() # время на конец операции
	timedelta = e - s #время начала минус время конца операции
	td = str(timedelta).split('.')[0] # разделяем результат по точке и выбираем первую часть (нулевой индекс)

    # Создаём лог-файл backup_log.txt
	log_filename = "backup_1C.log"
	log = open(log_filename, "a") # открываем файл-лог в режиме довления записи в конец файла
	log.write(today.strftime("%d.%m.%Y_%H.%M") + " Создан архив " + zip_name + "\n                 Размер архива: "+ convert_bytes(size) + ". Время выполнения: " + td + ".\n")
	log.close()

	# Сообщения, при успешном выполнении
	print(" Бэкап помещён в архив " + zip_name + "!")
	print(" Добавлена запись в лог-файл " + log_filename)
	print (" Операция выполнена за: " + td) # время выполнения программы
	print("")
	print(colored.green(" ГОТОВО!"))
input(" ")
