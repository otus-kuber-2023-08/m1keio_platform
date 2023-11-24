# m1keio_platform

<details closed>
  <summary>ДЗ 1</summary>

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

</details>

<details closed>
  <summary>ДЗ 2</summary>

#### Q: Описание ДЗ

#### A:

        1) Разобрали некоторые сущности в Kubernates такие как Deployment и Replicaset.
        2) Поиграли со стратегией релизов

</details>

<details closed>
  <summary>ДЗ 3</summary>

#### Q: Описание ДЗ

#### A:

        1) Разобрали некоторые сущности в Kubernates такие как Services и Ingress.
        2) Развернули MetalLB
        3) Натроили Ingress для деплоймента их ДЗ 1
        4) Пробросили наруду панель управлени
        5) Настроили canary-release

</details>

<details closed>
  <summary>ДЗ 4</summary>

#### Q: Описание ДЗ

#### A:

        1) Разобрали некоторые сущности в Kubernates такие как PV, PVC, StatefullSet и Secrets.
        2) Развернули MinIO как StateFullSet
        3) Настроили PV и PVC
        4) Унесли секреты от Minio в Secrets
        5) Все разобрали

</details>

<details closed>
  <summary>ДЗ 5</summary>

#### Q: Описание ДЗ
#### A:
        1) Посоздавали разные сервис аккаунты в разных скоупах
        2) Посоздавали роли с разными наборами прав
        3) Посоздавали RoleBindings между ролями и сервисаккаунтами
</details>

<details closed>
  <summary>ДЗ 6</summary>

#### Q: Описание ДЗ
#### A:
        1) Разобрались с cert-manager
        2) Подеплоили chartmuseum и harbor
        3) Кастомизировали helm chart hipster-shop
        4) Попробовали jsonnet, kuztomize
</details>

<details closed>
  <summary>ДЗ 7</summary>

#### Q: Описание ДЗ
#### A:
        1) Создали CRD,CR и необходимые ресурсы.
        2) Создали контроллер при помощи kopf framework
        3) Починили контроллер который криво создавал PVC.
     Q: Показать, что код работает
     A:
        ```
          ▶ kubectl get jobs.batch
            NAME                         COMPLETIONS   DURATION   AGE
            restore-mysql-instance-job   1/1           6s         16s
          ▶ kubectl get jobs.batch
            NAME                        COMPLETIONS   DURATION   AGE
            backup-mysql-instance-job   1/1           11s        26s
          private/m1keio_platform/kubernetes-operators  kubernetes-operators ✗                                                                                                                                 14h27m ⚑ ◒  ⍉
          ▶ kubectl exec -it $MYSQLPOD -- mysql -u root -potuspassword1 -e "CREATE TABLE test (id smallint unsigned not null auto_increment, name varchar(20) not null, constraint pk_example primary key (id) );" otus-database
          mysql: [Warning] Using a password on the command line interface can be insecure.

          private/m1keio_platform/kubernetes-operators  kubernetes-operators ✗                                                                                                                                  14h27m ⚑ ◒
          ▶ kubectl exec -it $MYSQLPOD -- mysql -potuspassword1 -e "INSERT INTO test ( id, name) VALUES ( null, 'some data' );" otus-database
          mysql: [Warning] Using a password on the command line interface can be insecure.

          private/m1keio_platform/kubernetes-operators  kubernetes-operators ✗                                                                                                                                  14h27m
          ▶ kubectl exec -it $MYSQLPOD -- mysql -potuspassword1 -e "INSERT INTO test ( id, name ) VALUES ( null, 'some data-2' );" otus-database
          mysql: [Warning] Using a password on the command line interface can be insecure.
          kubectl exec -it $MYSQLPOD -- mysql -potuspassword1 -e "select * from test;" otus-database
            mysql: [Warning] Using a password on the command line interface can be insecure.
            +----+-------------+
            | id | name        |
            +----+-------------+
            |  1 | some data   |
            |  2 | some data-2 |
            +----+-------------+
          KOPF logs:
          [2023-11-07 10:23:50,288] kopf.objects         [WARNING ] [default/mysql-instance] Patching failed with inconsistencies: (('remove', ('status',), {'kopf': {'progress': {'mysql_on_create': {'started': '2023-11-07T08:23:17.096469', 'stopped': '2023-11-07T08:23:44.767549', 'delayed': None, 'purpose': 'create', 'retries': 1, 'success': True, 'failure': False, 'message': None, 'subrefs': None}, 'update_object/spec.password': {'started': '2023-11-07T08:23:17.096490', 'stopped': None, 'delayed': None, 'purpose': 'create', 'retries': 0, 'success': False, 'failure': False, 'message': None, 'subrefs': None}}}}, None),)
          start deletion mysql-instance jobs
          password changed, diff: (('add', (), None, 'otuspassword1'),)
        ```
</details>

<details closed>
  <summary>ДЗ 8</summary>

#### Q: Описание ДЗ
#### A:
        1) Установили victoriametrics operator из
        https://github.com/VictoriaMetrics/helm-charts/blob/master/charts/victoria-metrics-operator/README.md
        2) Написали deployment с nginx и nginx-exporter и configmap для переопределения конфига.
        3) Добавили Service и ServiceMonitor
</details>

<details closed>
  <summary>ДЗ 9</summary>

#### Q: Описание ДЗ
#### A:
        1. Создан новый Helm chart для hipster-shop:

          ```bash
          helm create kubernetes-templating/hipster-shop
          ```

        2. Выполненные обновления и установки hipster-shop через Helm:

          - Установка и обновление hipster-shop в пространстве имен hipster-shop.

        3. Создан и обновлен Helm chart для frontend:

          ```bash
          helm create kubernetes-templating/frontend
          ```

        4. Обновление зависимостей для hipster-shop:

          ```bash
          helm dep update kubernetes-templating/hipster-shop
          ```

        5. Установлен Helm plugin для работы с секретами:

          ```bash
            helm plugin install https://github.com/futuresimple/helm-secrets
          ```

        6. Работа с VictoriaMetrics Operator:

          - Добавление репозитория victoriametrics, обновление репозиториев, поиск чартов VictoriaMetrics Operator и его установка в пространстве имен monitoring.

        7. Установка и обновление Elastic Stack компонентов:

          - Добавление репозитория elastic и установка Elasticsearch и Kibana в пространстве имен observability.

        8. Удаление и повторная установка Kibana с исправлениями:

          - Множественные попытки установки и удаления Kibana, включая очистку связанных ConfigMaps и других ресурсов.

        9. Работа с AWS Load Balancer Controller:

          - Установка и удаление aws-load-balancer-controller в пространстве имен kube-system.

        10. Работа с Fluent Bit:

          - Обновление чарта Fluent Bit и его настройка через файл значений.

        11. Установка и настройка Grafana:

          - Добавление репозитория grafana и настройка через файл значений.

        12. Работа с Prometheus Elasticsearch Exporter:

          - Установка и обновление Prometheus Elasticsearch Exporter с настройкой через файл значений.

        13. Работа с Vector:

          - Добавление репозитория vector и настройка чарта Vector для сбора и отправки логов.

        14. Установка и обновление Loki:

          - Установка и обновление чарта Loki от Grafana для управления логами.
</details>

