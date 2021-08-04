from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import schedule


print('¡Bienvenide a auto-ramos UC, el tomador de ramos automatico de la universidad!')
print('Creado con <3 por Dyotson (Max Militzer)\n')
print('FUNCIONAMIENTO:\n')
print('Primero tendras que ingresar tu usuario y contraseña UC, luego ingresaras tus NRC a tomar y ingresaras a que hora quieres tomar ramos.')
print('NO CIERRES EL PROGRAMA HASTA DESPUES DE TU TOMA DE RAMOS\n')
sistema = input('¿Cual es tu sistema operativo? (windows/linux): ')
while True:
    if sistema == 'windows' or sistema == 'linux':
        break
    sistema = input('¿Cual es tu sistema operativo? (windows/linux): ')
print('Testeando selenium driver, esto no tomara más de unos segundos...\n')
try:
    if sistema == 'linux':
        driver = webdriver.Firefox(executable_path='geckodriver')
    elif sistema == 'windows':
        driver = webdriver.Firefox(executable_path='geckodriver.exe')
    driver.get('https://www.google.com')
    driver.close()
except:
    print('Webdriver no se pudo ejecutar, porfavor revisa que tengas todos los componentes instalados.')
    exit()
print('\n')
print('Porfavor, ingresa tu usuario UC y contraseña: \n')
usuario = input('Usuario: ')
password = input('Contraseña: ')
NRC = input('Codigos NRC (Separados por un espacio): ')
NRC = NRC.split(" ")
hora = input('Ingresa la hora a la que tomaras ramos en formato 24hrs (Ej: 17:00 o 08:00): ')
while True:
    if len(hora) == 5:
        break
    print('Formato de hora incorrecto, recuerda agregar un 0 en caso de que sea en la mañana, ejemplo 08:00 en vez de 8:00')
    hora = input('Ingresa la hora a la que tomaras ramos en formato 24hrs (Ej: 17:00 o 08:00): ')
print('\n')
print('Toma agendada, recuerda no apagar ni cerrar el programa hasta que ocurra tu toma de ramos y el programa confirme que tomo tus ramos...')


def main():
    global usuario
    global password
    global NRC
    global sistema
    if sistema == 'linux':
        driver = webdriver.Firefox(executable_path='geckodriver')
    elif sistema == 'windows':
        driver = webdriver.Firefox(executable_path='geckodriver.exe')
    driver.get('https://ssb.uc.cl/ERPUC/twbkwbis.P_WWWLogin')
    # Inicio de sesion
    usuariobox = driver.find_element_by_xpath('//*[@id="UserID"]')
    passwordbox = driver.find_element_by_xpath('/html/body/div[3]/form/table/tbody/tr[2]/td[2]/input')
    loginbutton = driver.find_element_by_xpath('/html/body/div[3]/form/p/input')
    usuariobox.send_keys(usuario)
    passwordbox.send_keys(password)
    loginbutton.click()
    time.sleep(1)
    # Ingreso a pagina NRC
    try:
        agregarbutton = driver.find_element_by_xpath('/html/body/div[3]/table[2]/tbody/tr[2]/td[2]/a')
    except:
        driver.close()
        print('Usuario o contraseña incorrecta, favor intentar denuevo')
        usuario = input('Usuario: ')
        password = input('Contraseña: ')
        main()
    agregarbutton.click()
    time.sleep(1)
    enviarbutton = driver.find_element_by_xpath('/html/body/div[3]/form/input')
    enviarbutton.click()
    time.sleep(1)
    seleccionarlist = driver.find_element_by_xpath('//*[@id="st_path_id"]')
    seleccionarlist = Select(seleccionarlist)
    # No lo puedo testear pero por Dieguito Maradona que funcione BEGIN
    planes = seleccionarlist.options
    planes = planes[1:]
    print('Se encontraron los siguientes planes de estudios:')
    for i in range(len(planes)):
        print(str(i) + ": " + planes[i])
    try:
        planseleccionado = int(input('Ingresa el numero del plan de estudios para el que quieres tomar ramos: '))
        assert isinstance(planseleccionado, int)
        assert planseleccionado <= len(planes)
        seleccionarlist.select_by_index(planseleccionado)
    except:
        print('Error: Plan de estudios no válido, recuerda ingresar el numero del plan de estudios para el que quieres tomar ramos')
        nuevoplanseleccionado = int(input('Ingresa el numero del plan de estudios para el que quieres tomar ramos: '))
        assert nuevoplanseleccionado <= len(planes)
        seleccionarlist.select_by_index(nuevoplanseleccionado)
    # No lo puedo testear pero por Dieguito Maradona que funcione END
    enviarplan = driver.find_element_by_xpath('/html/body/div[3]/form/input[19]')
    enviarplan.click()
    time.sleep(1)
    # Ingreso a plataforma de ramos
    i = 1
    while i <= 3:
        if i == 1:
            nrc1 = driver.find_element_by_xpath('//*[@id="crn_id1"]')
            nrc1.send_keys(NRC[0])
        elif i == 2 and len(NRC) >= 2:
            nrc2 = driver.find_element_by_xpath('//*[@id="crn_id2"]')
            nrc2.send_keys(NRC[1])
        elif i == 3 and len(NRC) == 3:
            nrc3 = driver.find_element_by_xpath('//*[@id="crn_id3"]')
            nrc3.send_keys(NRC[2])
        i += 1
    enviarcambios = driver.find_element_by_xpath('/html/body/div[3]/form/input[19]')
    enviarcambios.click()
    print('¡Ramos tomados! Ya es seguro cerrar la aplicacion...')


schedule.every().day.at(hora).do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
