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

<details closed>
  <summary>ДЗ 10</summary>

#### Q: Описание ДЗ

#### A:

        1. Создали кластер EKS используя pulumi. [source]{https://gitlab.com/1474/pulumi-eks-otus}
        2. Cобрали и запушили докер образы из src/**/Dockerfile.
        3. Установили Flux, но не v1 а v2.
          ```
          kubectl apply -f https://raw.githubusercontent.com/fluxcd/helmoperator/master/deploy/flux-helm-release-crd.yaml
          curl -s https://fluxcd.io/install.sh | sudo bash\n
          omz plugin enable fluxcd
          export GITLAB_TOKEN=123
          flux bootstrap gitlab --deploy-token-auth --owner=1474  --repository=microservices-demo --branch=main --path=deploy --personal
          ```
        4. Настроили установку, слежение и автообновление релиза через GitRepository, HelmRelease, ImageRepository,ImagePolicy, ImageUpdateAutomation
        5. Настроили мониторинг через Victoria Metrics Operator при помощи VMCluster, VMAgent, VMServiceScrape, VMPodScrape
        6. Добавили Grafana через Helm.
        7. Настроили Canary через Flagger.
          ```
          kubectl get canaries -n microservices-demo
            NAME       STATUS      WEIGHT   LASTTRANSITIONTIME
            frontend   Succeeded   0        2023-11-27T16:22:23Z
          kubectl describe canaries frontend -n microservices-demo
            ...
            Events:
              Type     Reason  Age                     From     Message
              ----     ------  ----                    ----     -------
              Normal   Synced  3m45s (x6 over 2d22h)   flagger  New revision detected! Scaling up frontend.microservices-demo
              Normal   Synced  3m15s (x6 over 2d22h)   flagger  Starting canary analysis for frontend.microservices-demo
              Normal   Synced  3m15s (x2 over 70m)     flagger  Advance frontend.microservices-demo canary weight 50
              Warning  Synced  2m45s (x21 over 2d22h)  flagger  Halt advancement no values found for istio metric request-success-rate probably frontend.microservices-demo is not receiving traffic: running query failed: no values found
              Normal   Synced  2m15s (x2 over 70m)     flagger  Copying frontend.microservices-demo template spec to frontend-primary.microservices-demo
              Normal   Synced  105s (x2 over 69m)      flagger  Routing all traffic to primary
              Normal   Synced  75s (x2 over 69m)       flagger  Promotion completed! Scaling down frontend.microservices-demo
          ```

</details>

<details closed>
  <summary>ДЗ 11</summary>
Установка Vault

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm search repo hashicorp/vault
helm install vault hashicorp/vault
```

Статусы волта

```bash

kubectl exec -it vault-0 -- vault status
Key Value

---

Seal Type shamir
Initialized true
Sealed false
Total Shares 1
Threshold 1
Version 1.15.2
Build Date 2023-11-06T11:33:28Z
Storage Type consul
Cluster Name vault-cluster-3448a1cc
Cluster ID 026604f0-e988-ee70-85f3-2b222cef3433
HA Enabled true
HA Cluster https://vault-0.vault-internal:8201
HA Mode active
Active Since 2023-11-30T19:48:24.737276345Z
```

Генерация секретов

```bash

kubectl exec -it vault-0 -- vault login
Token (will be hidden):
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key Value

---

token hvs.sZU9wJU59KxncV0rkLzf2ufa
token_accessor 20YvKTUxmGDBVeyUfzKkjIrl
token_duration ∞
token_renewable false
token_policies ["root"]
identity_policies []
policies ["root"]

---
```

Список энжинов

```bash
kubectl exec -it vault-0 -- vault auth list
Path Type Accessor Description Version

---

## token/ token auth_token_7db19ff6 token based credentials n/a

```

Секреты

```bash

kubectl exec -it vault-0 -- vault read otus/otus-ro/config
Key Value

---

refresh_interval 768h
password asajkjkahs
username otus

---

kubectl exec -it vault-0 -- vault kv get otus/otus-rw/config
====== Data ======
Key Value

---

password asajkjkahs
username otus

```

Новый список авторизаций

```bash

kubectl exec -it vault-0 -- vault auth list
Path Type Accessor Description Version

---

kubernetes/ kubernetes auth_kubernetes_3171bc41 n/a n/a
token/ token auth_token_7db19ff6 token based credentials n/a
```

Исправленные экспорты

```bash
export SA_SECRET_NAME=$(kubectl get secrets --output=json| jq -r '.items[].metadata | select(.name|startswith("vault-auth-")).name')
export SA_JWT_TOKEN=$(kubectl get secret $SA_SECRET_NAME --output 'go-template={{ .data.token }}' | base64 --decode)
export SA_CA_CRT=$(kubectl config view --raw --minify --flatten --output 'jsonpath={.clusters[].cluster.certificate-authority-data}' | base64 --decode)
export K8S_HOST=$(kubectl config view --raw --minify --flatten --output 'jsonpath={.clusters[].cluster.server}')
kubectl exec -it vault-0 -- vault write auth/kubernetes/config \ token_reviewer_jwt="$SA_JWT_TOKEN" \
kubernetes_host="$K8S_HOST" \
kubernetes_ca_cert="$SA_CA_CRT" \
issuer="https://kubernetes.default.svc.cluster.local"
```

Создаем контейнер с сервис-аккаунтом

```bash

kubectl run --image alpine:3.7 --overrides='{ "spec": { "serviceAccount": "vault-auth" } }' --rm -it -- sh

curl --request POST --data '{"jwt": "'$KUBE_TOKEN'", "role": "otus"}' $VAULT_ADDR/v1/auth/kubernetes/login | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1796  100   749  100  1047   1079   1508 --:--:-- --:--:-- --:--:--  2584
{
  "request_id": "6f53a706-f626-7aef-1a3b-5f75168ffb2f",
  "lease_id": "",
  "renewable": false,
  "lease_duration": 0,
  "data": null,
  "wrap_info": null,
  "warnings": null,
  "auth": {
    "client_token": "hvs.CAESIO8s1DCEU-gsOWLURjLLMDRmMN8KeAeiiU-9oBGsUI89Gh4KHGh2cy44SUl6TVA0M2dnUlB1U0Vyb203TUlPWGg",
    "accessor": "idsCFjtK8buSTFuYgbKZ5FiA",
    "policies": [
      "default",
      "otus-policy"
    ],
    "token_policies": [
      "default",
      "otus-policy"
    ],
    "metadata": {
      "role": "otus",
      "service_account_name": "vault-auth",
      "service_account_namespace": "default",
      "service_account_secret_name": "",
      "service_account_uid": "110f0cc8-6983-44b3-8fae-843a5606dda4"
    },
    "lease_duration": 86400,
    "renewable": true,
    "entity_id": "56f10ceb-09f6-4d73-0cd3-eb1c770aaf72",
    "token_type": "service",
    "orphan": true,
    "mfa_requirement": null,
    "num_uses": 0
  }
}

```

Q: Почему мы смогли записать otus-rw/config1 но не смогли otusrw/config

A: Для записи в otus-rw нужна capability `update`.

```bash

path "otus/otus-rw/*" {
capabilities = ["read", "create", "list", "update"]
}

```

PKI

```bash

kubectl exec -it vault-0 -- vault write pki_int/issue/example-dot-ru common_name="gitlab.example.ru" ttl="24h"
Key                 Value
---                 -----
ca_chain            [-----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUDwY0KIkUmbPZzDov3/LpXUQA/jkwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0yMzExMzAyMTQzNDFaFw0yODEx
MjgyMTQ0MTFaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJ8owOWVfjnJ
L+Yc6HCBasJFTNh6qkErG/9wM3s4xWbJ/rt2gtlBruY9tdh2SVaTnQ6xppjR2/MB
PUTg3TeP7b93JUGQG9aONxxw7fD25sxyTTVvkEpthu2a7rpgmTOtcKESvcNQ7opA
w29RMVvAoUdQzN8yh4ZeYHmcY0Z6PuHK8Rotvbgb5pLHOBMbYIwjyK38ZPZyllSg
nW0G+7pEhHgbtUwG7+bNUtH1puJgR4bp4nRfWOwhYHLXWkfKf7JlnYpMzuJbBTxa
2EalmTfgxJoS+xKzYmm9MzQMF0dvNKpitmj1bgfPiJ54k9o86bIahEfvCMjTaofK
0u5fbXJdl1ECAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQU4szV65ObFJ2cLJD/+hOH761QUyAwHwYDVR0jBBgwFoAU
HN6FCng3R1IqvselS6vUDgd7rOEwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
FQR/px4WQYlvetU6AWTjjclOo9892f06PAOMyNp9GBa7Qa6//pizGN5kbXscyHqA
tL/hFlIJ9QSdzHa4A7/tDG0FS1ldCkvalbby43vTlx+ZBQeFRGlR3IPEyCcoC1Bn
VJxzrhrHo8S8OxbhMgqWUSynwgnOkKGk5XnnMPhOMd2sziDO4+ogicoz0cyZEQ6L
4AghRKv9OGi9s9XodP1to2cW7GPkWFRV5zyHB8bEiTtbFwnSKlsGuMCntUTgIcJW
uN2xtNwByGKaPqnc8JK7ojGHaVZTh3HeJsN0G3oW8Dz04d9Ibbcu1NtD3JGS30DX
9VGw9zHawoI0htzid1ioSg==
-----END CERTIFICATE----- -----BEGIN CERTIFICATE-----
MIIDMjCCAhqgAwIBAgIUSll05UR2JuvhgL6hPUWJy/rffmkwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0yMzExMzAyMTQwNDdaFw0zMzEx
MjcyMTQxMTZaMBUxEzARBgNVBAMTCmV4bWFwbGUucnUwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQC/1xBIgSicLN5CHd8Os4aGYAf8/w6rylpy5j0Er1MZ
aTSSJH6+D+NovQycwJw9WntKJcih6qe6Gqbj+/L5OR6Ub70pOQoYHA2M9NKiLE/A
NE/UqgslfCSO1VPAQHNYb//G1+EqCJwOOT4LKDyV45HF/kX8G+G7SfsZfO71ldaE
y+VEd0fK57h55C3GaxDxyTI/kzKd8aLmg/fqAT57bxzUcuWu1d6fgDNlaSrcIt9s
yFS3p479cB0f38E+mt/k7ZbIuEmGMSys9kBokfLkf5FHUtdV80Nh83Ws05RLVo6T
fskMfQgUyS24FkoAa3RyzfMhqlUwusilX/FunPbJ6xeLAgMBAAGjejB4MA4GA1Ud
DwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBQc3oUKeDdHUiq+
x6VLq9QOB3us4TAfBgNVHSMEGDAWgBQc3oUKeDdHUiq+x6VLq9QOB3us4TAVBgNV
HREEDjAMggpleG1hcGxlLnJ1MA0GCSqGSIb3DQEBCwUAA4IBAQB2f+KbSHsGzfPe
vFi37Yngl4vzqkFC2mu2vkdT/1inr37EKp4FeTaOtWX+K/5pfS4cqUGcWzBJ9Gyv
1v9AT4eH+AWyetvoQGwZXgMi1uzrIEkRlHBGsaftQ8eeAAhz/6o4Tsecr9yAJF+T
nDbTLgfTs8GxRl540dWUn0Ki9a1eePrqnLIls+KrPNuxSIfTVPx/6cSmk5PpwCcH
+TjjXxs98XYXv1+Y8VvXX4pRuVgi5rh6x2r6LGwiowTfYH2F5xEvvNtvCWh/B4hd
hKy2QB2EU4ao0wojIIm+PlBynobJmyRWs+F9PIw1Kz4+K9WU7Qw7HSx7aAiVZobX
etd/lD0m
-----END CERTIFICATE-----]
certificate         -----BEGIN CERTIFICATE-----
MIIDZzCCAk+gAwIBAgIULrcA2g0ZTC9XAbMRGnimVDK+OSwwDQYJKoZIhvcNAQEL
BQAwLDEqMCgGA1UEAxMhZXhhbXBsZS5ydSBJbnRlcm1lZGlhdGUgQXV0aG9yaXR5
MB4XDTIzMTEzMDIxNDk0M1oXDTIzMTIwMTIxNTAxM1owHDEaMBgGA1UEAxMRZ2l0
bGFiLmV4YW1wbGUucnUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDy
vt7qej880G75wodu9rvejpCg0I2gOl5CYwAetfLfpPY/8I/JgJNA+OjpeiYNVb8T
gkjZabgyZelX/uhpIWLCd79r0yUVfLzk4cL9T99rz6+Rf7c2Axam1Z48Qdvu/FPG
xyt+MiSs47i12VthzQdPuiOYfWmQzEUoGmUJBYjnakUyreZ9w8mko75lT/4ORSXH
4BW3L12VrahQarU21o99c4To2OVBuNonuevk/20OuPKiXqB/OFiFUSg+v76OMrwq
WqNJpeswYGX4ts946TAHP61Phy3e0byhUii0RJvyu7baeq3X6u5R9KDSpiCA6F+O
0nRWKsocIx6gnsIJ43+/AgMBAAGjgZAwgY0wDgYDVR0PAQH/BAQDAgOoMB0GA1Ud
JQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAdBgNVHQ4EFgQUAI/Pb/CFj6qLbFhR
aLJI0LOQTsYwHwYDVR0jBBgwFoAU4szV65ObFJ2cLJD/+hOH761QUyAwHAYDVR0R
BBUwE4IRZ2l0bGFiLmV4YW1wbGUucnUwDQYJKoZIhvcNAQELBQADggEBAF4vpEln
bTXzvhb6GCdZ8lhpu98U8UdsaZ5Zug1D07hcWxtzcKsxABrdwKrTf8WUvQKTI4rH
E+do4GRhBUqVRqYZ3uIs0oLN7b6HgUIAqieQxdFlXg+D93dwfX8ZyWC9W1qNKlXM
kUuo04QQ1K9UpJY+8O4+Z6frWPbj/Ffegh77IhnfldSXJAT3ydmo1EgQhucyrwDE
xDd1PTUQk9226SjeC7rlEe+G+vYQwX1DSMFU4wbrBoQxCWVx2NZ7/9GLdRUwUrTz
sm6C7G9LAorya02rChLPDQCPMKmcokcaMGE9kMC+9Gekv3CaWMkTraVzxqErYRrm
2U4DDjq3YOlzQ68=
-----END CERTIFICATE-----
expiration          1701467413
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUDwY0KIkUmbPZzDov3/LpXUQA/jkwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0yMzExMzAyMTQzNDFaFw0yODEx
MjgyMTQ0MTFaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJ8owOWVfjnJ
L+Yc6HCBasJFTNh6qkErG/9wM3s4xWbJ/rt2gtlBruY9tdh2SVaTnQ6xppjR2/MB
PUTg3TeP7b93JUGQG9aONxxw7fD25sxyTTVvkEpthu2a7rpgmTOtcKESvcNQ7opA
w29RMVvAoUdQzN8yh4ZeYHmcY0Z6PuHK8Rotvbgb5pLHOBMbYIwjyK38ZPZyllSg
nW0G+7pEhHgbtUwG7+bNUtH1puJgR4bp4nRfWOwhYHLXWkfKf7JlnYpMzuJbBTxa
2EalmTfgxJoS+xKzYmm9MzQMF0dvNKpitmj1bgfPiJ54k9o86bIahEfvCMjTaofK
0u5fbXJdl1ECAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQU4szV65ObFJ2cLJD/+hOH761QUyAwHwYDVR0jBBgwFoAU
HN6FCng3R1IqvselS6vUDgd7rOEwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
FQR/px4WQYlvetU6AWTjjclOo9892f06PAOMyNp9GBa7Qa6//pizGN5kbXscyHqA
tL/hFlIJ9QSdzHa4A7/tDG0FS1ldCkvalbby43vTlx+ZBQeFRGlR3IPEyCcoC1Bn
VJxzrhrHo8S8OxbhMgqWUSynwgnOkKGk5XnnMPhOMd2sziDO4+ogicoz0cyZEQ6L
4AghRKv9OGi9s9XodP1to2cW7GPkWFRV5zyHB8bEiTtbFwnSKlsGuMCntUTgIcJW
uN2xtNwByGKaPqnc8JK7ojGHaVZTh3HeJsN0G3oW8Dz04d9Ibbcu1NtD3JGS30DX
9VGw9zHawoI0htzid1ioSg==
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA8r7e6no/PNBu+cKHbva73o6QoNCNoDpeQmMAHrXy36T2P/CP
yYCTQPjo6XomDVW/E4JI2Wm4MmXpV/7oaSFiwne/a9MlFXy85OHC/U/fa8+vkX+3
NgMWptWePEHb7vxTxscrfjIkrOO4tdlbYc0HT7ojmH1pkMxFKBplCQWI52pFMq3m
fcPJpKO+ZU/+DkUlx+AVty9dla2oUGq1NtaPfXOE6NjlQbjaJ7nr5P9tDrjyol6g
fzhYhVEoPr++jjK8KlqjSaXrMGBl+LbPeOkwBz+tT4ct3tG8oVIotESb8ru22nqt
1+ruUfSg0qYggOhfjtJ0VirKHCMeoJ7CCeN/vwIDAQABAoIBAHGkC8Xnzx0QUzPX
7wFyvwb05R50JCljyeb4ZAD8myQ6HRJX82iZKdbb8GYFSjUp9FcUwjgONy5Y6YHJ
k1JMT+jMmK/I3G6Pw/q++kMOloDpbL8H9GRz07HtBbQd/PGH7Ux8x46/uM27miiA
Bjjl/EtF0A4+gCJKjwG0QaKUlcAH5c4fJO5EFdvN4hMj6eSHdyK2J5qmiAR5AE6/
poW5/EwL0aR4MnaJm2sE5nPkj4iwsiMywzxxSMdgUSVc720k0MVT2FKW2R+SF/iE
q/MRXQbc8Ppp5AS8TyU4oBNGpQJ1FnzALp3fX7HATHif2DVKKyH9HsOEoJRpSNbW
5RkmdUECgYEA9/wwIcBIrXd9rfcWz0npEx1twjByjR0Et29NMRqWEhsTw9I391BE
iClWauBvNOSDRC+eyZnuu73CrUmUvRGUewt+ezFFcPG/DXxXtE+I5kO4e+WzhjO6
v1tBd47j4V1U2GEW/yLZE0eVCc7I3HIXTtlGRpYCSc1OqkB0hmwqrh8CgYEA+pdU
0Os7As/OreN7DKL9Q4BXOPpCEdIoHvLBNHblZiEmCrq/JLTinngKXKPZSryCmwQg
Xd+mq54rffBrbDR3Ww+EylBwMyrnRYX4Ulve9v+c7AOU1pkBes27I6RmV4gxTS7H
341cb+/U2GHOUsI9xlakQufOJwCoI04V/bQrumECgYEAuxskldKnA3ss8J2GMFDr
8ug5cFNtmttSO7VW4L3WjUKw3wc2AvwlOTc3ZNyCC75+7GuhuyrR3gWHZYgnGaCy
D0TU4c6DPnyoUlyHMBzyhgqCn7jog1F0jf0koDjH57qr0bcvysFYWBuicAv9sZbD
z1JQm+GDSHwH5p1LTkE+0rECgYEAhsPN5FEtOjTh1Nhqu4AILj4eKlFEKOtZklNB
HmL2ubcIC2slEquI2Gp8QBgJ6sx4fL96XKHDs7Xrc95RFy8cJUeyRU9/F7VyDQyg
YEJyJWmQTckbSVGd3xo3E1L9iwN+aCDJcutGFBjp4bivyggWSs0bp7OcRZNv2RTM
dNVpUuECgYBqDmg8sUgnjJpb8SQ6KbNtzsxrMZppNO8XEQws4lj47+JpW9kKPweX
f7JkUjO+z+5bwpDqtERLrmQ888szs1r01P4y9s6Id58O47DfoNDJr1+/KV9gyyHH
0tczop9v//45PtuiLDbyAdLZ7YH9Cb+fAM06on51Mb4hS7iZLcICkA==
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       2e:b7:00:da:0d:19:4c:2f:57:01:b3:11:1a:78:a6:54:32:be:39:2c
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
kubectl exec -it vault-0 -- vault write pki_int/revoke serial_number='2e:b7:00:da:0d:19:4c:2f:57:01:b3:11:1a:78:a6:54:32:be:39:2c'
Key                        Value
---                        -----
revocation_time            1701381051
revocation_time_rfc3339    2023-11-30T21:50:51.249457755Z
state                      revoked
-------------------------------------------------------------------------------------------
```

</details>


<details closed>
  <summary>ДЗ 12</summary>

* Deploy CSI HostPath Driver
```bash

git clone https://github.com/kubernetes-csi/csi-driver-host-path.git
cd csi-driver-host-path
cd deploy
cd kubernetes-latest
./deploy.sh

```

* Create storage class

```bash

kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/csi-driver-host-path/master/examples/csi-storageclass.yaml

```

* Create PVC

``` bash

kubectl apply -f pvc.yaml

```


* Create Pod

```bash

kubectl apply -f pod.yaml

```

* events:

```bash
kubectl events

...
8m20s                  Normal    ProvisioningSucceeded     PersistentVolumeClaim/storage-pvc                          Successfully provisioned volume pvc-38149df5-f853-4aa1-8b59-3817c11a5371
8m20s                  Normal    Provisioning              PersistentVolumeClaim/storage-pvc                          External provisioner is provisioning volume for claim "default/storage-pvc"
8m9s                   Normal    SuccessfulAttachVolume    Pod/storage-pod                                            AttachVolume.Attach succeeded for volume "pvc-38149df5-f853-4aa1-8b59-3817c11a5371"
8m9s                   Normal    Scheduled                 Pod/storage-pod                                            Successfully assigned default/storage-pod to kind-control-plane
7m59s                  Normal    Pulling                   Pod/storage-pod                                            Pulling image "nginx"
7m37s                  Normal    Created                   Pod/storage-pod                                            Created container webpod
7m37s                  Normal    Started                   Pod/storage-pod                                            Started container webpod
7m37s                  Normal    Pulled                    Pod/storage-pod                                            Successfully pulled image "nginx" in 16.219496767s (21.63391741s including waiting)


```

</details>
