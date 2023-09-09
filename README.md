# m1keio_platform

## ДЗ 1

#### Q:

    Для выполнения домашней работы необходимо создать Dockerfile, в
    котором будет описан образ:
    1. Запускающий web-сервер на порту 8000 (можно использовать любой
    способ);
    2. Отдающий содержимое директории /app внутри контейнера (например,
    если в директории /app лежит файл homework.html , то при запуске
    контейнера данный файл должен быть доступен по URL
    http://localhost:8000/homework.html );
    3. Работающий с UID 1001.

#### A:

    Dockerfile - создан на базе python simplehttpserver.

#### Q:

    В README.md нужно внести описание проделанной работы

#### A:

        1) Создан minikube cluster
        2) Подготовлен Dockerfile
        3) Docker-образ залит в Registry
        4) Подготовлен Kubernates Pod манифест web-pod.yaml
           запускающий вебсервис в кластере minikube на базе
           предварительно собранного образа
        5) В манифест добавлен init-container для добавления контентного файла для web-сервера
        6) Визуально проверена работоспособность приложения при помощи проброса внутреннего адреса
           Pod в сеть рабочей станции.
        7) Собран и опубликован в  Registry образ микросерфиса frontend из репозитория Hipster Shop
        8) В кластере k8s запущен контейнер на базе опубликованного ранее образа при помощи ad-hoc.
        9) Из ad-hoc команды получен манифест и исправлен для устранения ошибки при запуске Pod.(добавлены переменные окружения)