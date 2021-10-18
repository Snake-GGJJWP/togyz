Для того, чтобы запустить приложение сейчас необходимо следовать следующим инсрукциям:
1. Скачайте версию python 3.9.6 для вашей системы с официального сайта https://www.python.org/downloads/release/python-396/  (рекомендуется) или любую другую версию новее.
1. Установите python и добавьте python в переменную PATH (обязательно!!!) (https://www.istocks.club/%D0%BA%D0%B0%D0%BA-%D0%B4%D0%BE%D0%B1%D0%B0%D0%B2%D0%B8%D1%82%D1%8C-python-%D0%B2-%D0%BF%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D1%83%D1%8E-path-windows/2020-10-14/)
1. Скачайте библиотеку django 
	- Для Windows: пропишите в командной строке python -m pip install django(https://docs.djangoproject.com/en/1.8/howto/windows/)
	- Для MacOS: пропишите в терминале python3 -m pip install django
	- Для Linux (Ubuntu): пропишите в терминале pip3 install django
	- P.S. Если не можете установить, значит вы не установили pip (смотрите в гугле "как установить pip для <ваша система>")
	- P.P.S. Если не получается, смотрите в гугле по коду ошибки (если вы не разбираетесь в этом, попросите это сделать того, кто разбирается)
	1. Убедитесь, что django работает корректно. Для этого пропишите django-admin --version в вашей командной строке или терминале. Если выведет что-то вроде этого, значит django установлен правильно.
 ![image](https://user-images.githubusercontent.com/60911417/137697576-6079a83a-615a-4bab-b976-1d6ff6f1d063.png)

	1. Ещё один способ убедиться в этом - запустить среду python в командной строке или терминале (https://www.datacamp.com/community/tutorials/running-a-python-script) и пропишите import django; django.__version__. Если получилось что-то вроде этого, значит django установлен правильно.
![image](https://user-images.githubusercontent.com/60911417/137697681-b3579bee-6907-4015-8ebf-fa5e0d30dcb9.png)

1. Скачать библиотеку channels 
	- Для Windows: прописать в командной строке python -m pip install -U channels
	- Для MacOS: прописать в терминале python3 -m pip install -U channels
	- Для Linux (Ubuntu): прописать в терминале pip3 install -U channels
	1. Убедитесь, что channels работает правильно. Для этого запустите среду python в командной строке или терминале (как в пункте 3.2) и пропишите import channels; channels.__version__ . Если получилось что-то вроде этого, то channels установлен правильно.
![image](https://user-images.githubusercontent.com/60911417/137697901-090d82cc-35b5-4610-b7d7-5d2fc2e7f893.png)

1. Скачать библиотеку channels_redis
		a. Для Windows: прописать в командной строке python -m pip install channels_redis
		b. Для MacOS: прописать в терминале python3 -m pip install channels_redis
		c. Для Linux (Ubuntu): прописать в терминале pip3 install channels_redis
	1. Убедитесь, что channels_redis работает правильно. Для этого запустите среду python в командной строке или терминале (как в пункте 3.2) и пропишите import channels_redis; channels_redis.__version__ . Если получилось что-то вроде этого, то channels_redis установлен правильно.
![image](https://user-images.githubusercontent.com/60911417/137698006-e246ee5f-c0b7-41d5-9718-32c586b1c9e2.png)

1. Скачать и запустить сервер Redis
	- Для Windows: скачайте и установите последнюю версию по этой ссылке https://github.com/tporadowski/redis/releases. Рекомендуется устанавливать с .msi файла. При установке с .msi не забудьте установить галочку на "Add the Redis installation folder to the PATH enviroment variable". Если вы скачали portable, то вручную добавьте папку Redis в переменную PATH и прописать в командной строке redis-server.
	- Для MacOS: следуйте инструкции по этой сслыке https://phoenixnap.com/kb/install-redis-on-mac (гугл переводчик в помощь)
	- Для Linux: следуйте инструкции на официальном сайте https://redis.io/download (гугл переводчик в помощь)
	1. Убедитесь, что сервер запущен. Для этого в командной строке/терминале введите redis-cli и далее set v 'foo'. Если вывело что-то вроде этого, значит все работает.
  ![image](https://user-images.githubusercontent.com/60911417/137698133-3a9bfd5c-469e-466f-8ff7-a56715dace8e.png)

1. Можете сделать перерыв, если вы устали следовать этой инструкции. Инструкция подождёт.
1. Отдохнули? Тогда скачиваем репозиторий в удобную вам папку. Убедитесь что скачиваете правильную версию с ветки main. Репозиторий можете скачать через zip или с помощью git bash.
1. Открываем терминал или командную строку в папке с приложением. Для этого откройте командную строку или терминал и пропишите cd "путь/до/папки/с/приложением".
1. Запустите сервер на localhost.
	- Для Windows: в открытой командной строке пропишите python manage.py runserver 127.0.0.1:8000
	- Для MacOS: в открытом терминале пропишите python3 manage.py runserver 127.0.0.1:8000
	- Для Linux (Ubuntu): в открытом терминале пропишите python3 manage.py runserver 127.0.0.1:8000 
	1. Убедитесь, что сервер работает корректно. Если в открытой командной строке или терминале у вас что-то вроде этого, значит сервер запущен нормально. Поздравляю, вы великолепны!
![image](https://user-images.githubusercontent.com/60911417/137698319-b5ef2907-d321-4e93-a590-85f6ba3afde7.png)

	- **P.S.** Если предыдущие пункты были выполнены правильно, то приложение будет работать стабильно. К сожалению, такой запуск тестировался только на Windows10 x64, поэтому, если вы на другой системе и что-то пошло не так, то лучше найти машину с Windows10 x64. Приношу извинения за неудобства.
