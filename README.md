Развертывание сервера:

1) Установите python, flask и модули.
	sudo apt install python3 python3-flask python3-pip
	sudo pip install werkzeug requests
        sudo apt install nginx gunicorn
2) Скопируйте содержимое файла server.py в главный файл приложения. Измените ip на ip своей машины.
3) Скопируйте содержимое файла wsgi.py, если меняли имя главного файла, измените его и тут.
4) Создайте server.service командой "sudo nano /etc/systemd/system/server.service" и скопируйте в него содержимое соответствующего файла. Подправьте пути и имена.
5) Создайте страницу в nginx "sudo nano /etc/nginx/sites-available/server". Cкопируйте туда содержимое server.
6) Проверьте service файл. Введите "sudo systemctl start server", если вы сделали все правильно, в папке приложения должен появится сокет файл.
7) Сделайте символическую ссылку на nginx файл
	sudo ln -s /etc/nginx/sites-available/server /etc/nginx/sites-enabled/server
8) Проверьте конфигурацию nginx
	sudo nginx -t
9) Если все прошло успешно, перезапустите nginx.
	sudo service nginx restart
10) Добавьте server в автозагрузку, чтобы сервер автоматически запускался.
	sudo systemctl enable server


Использование сервера:

1) Установите python и модули.
	sudo apt install python3 python3-pip
	sudo pip install requests
2) Создайте python файл и скопируйте туда содержимое client.py. Измените ip на ip вм, на которой развернут сервер.
3) Запустите файл и следуйте инструкциям.
