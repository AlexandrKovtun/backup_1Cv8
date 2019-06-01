
from datetime import datetime
from os import remove, system, path
import zipfile
from clint.textui import colored # модуль для печати разными цветами
from time import gmtime, strftime

system("mode con cols=65 lines=17") # задаём размер окна консоли

print("")
print("           РЕЗЕРВНОЕ КОПИРОВАНИЕ ФАЙЛА БАЗЫ 1Cv8.1CD")
print(" =============================================================== ")

today = datetime.today() # получаем текущую дату

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
	start_time = datetime.today() # начинаем отсчёт времени today.strftime("%d.%m.%Y_%H.%M", gmtime())
	filename2 = input(' Введите префикс бэкапа или нажмите "ENTER":\n ')
	if filename2 == "":
		filename2 = "backup_" + today.strftime("%d.%m.%Y_%H.%M") + "_" + filename1
	else:
		filename2 = filename2 + "_" + today.strftime("%d.%m.%Y_%H.%M") + "_" + filename1	
	file2 = open(filename2,"wb")
	print(" Копирование начато! Ожидайте...")
	file2.write(file1.read())				# копирование
	file1.close()							# закрываем файлы
	file2.close()
	print(" Копирование успешно завершено!")
	print(" Был создан файл " + filename2)

	# упаковываем в архив созданную копию файла
	print(" Начата упаковка файла в zip-архив! Ожидайте...")
	zip_name = filename2 + ".zip"
	my_zip = zipfile.ZipFile(zip_name, 'w')
	my_zip.write(filename2, compress_type=zipfile.ZIP_DEFLATED)
	my_zip.close()

	remove(filename2) # удаляем созданную копию файла

	size = path.getsize(zip_name) # получаем размер файла

    # Создаём лог-файл backup_log.txt
	log_filename = "backup_1C.log"
	log = open(log_filename, "a")
	log.write(today.strftime("%d.%m.%Y_%H.%M") + " Создан архив " + zip_name + "\n                 Размер архива: "+ convert_bytes(size) + ". Время выполнения: " + str(datetime.today() - start_time) + ".\n")
	log.close()

	# Сообщения, при успешном выполнении
	print("")
	print(" Бэкап помещён в архив " + zip_name + "!")
	print(" Добавлена запись в лог-файл " + log_filename)
	print (" Операция выполнена за: " + str(datetime.today() - start_time)) # время выполнения программы
	print("")
	print(colored.green(" ГОТОВО!"))
	
input(" ")
