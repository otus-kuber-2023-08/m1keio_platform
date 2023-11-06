import kopf
import yaml
import kubernetes
import time
from jinja2 import Environment, FileSystemLoader


def render_template(filename, vars_dict):
    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template(filename)
    yaml_manifest = template.render(vars_dict)
    json_manifest = yaml.load(yaml_manifest, Loader=yaml.SafeLoader)
    return json_manifest


def delete_successful_jobs(mysql_instance_name):
    print(f'start deletion {mysql_instance_name} jobs')  # noqa: E501
    api = kubernetes.client.BatchV1Api()
    jobs = api.list_namespaced_job('default')
    for job in jobs.items:
        jobname = job.metadata.name
        if jobname in [f'backup-{mysql_instance_name}-job',
                       f'restore-{mysql_instance_name}-job',
                       f'change-password-{mysql_instance_name}-job']:
            if job.status.succeeded == 1:
                api.delete_namespaced_job(
                    jobname, 'default', propagation_policy='Background')


def wait_until_job_end(jobname):
    api = kubernetes.client.BatchV1Api()
    job_finished = False
    jobs = api.list_namespaced_job('default')
    while not job_finished and any(
            job.metadata.name == jobname for job in jobs.items):
        time.sleep(1)
        jobs = api.list_namespaced_job('default')
        for job in jobs.items:
            if job.metadata.name == jobname:
                print(f'job with name {jobname} found, waiting until end')
                if job.status.succeeded == 1:
                    print(f'job with {jobname} is successful')
                    job_finished = True


@kopf.on.create('otus.homework', 'v1', 'mysqls')
def mysql_on_create(body, spec, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']
    storage_size = body['spec']['storage_size']
    # Генерируем JSON манифесты для деплоя
    persistent_volume_claim = render_template('mysql-pvc.yml.j2',
                                              {'name': name,
                                               'storage_size': storage_size})
    service = render_template('mysql-service.yml.j2', {'name': name})

    deployment = render_template('mysql-deployment.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})

    restore_job = render_template('restore-job.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})

    # Определяем, что созданные ресурсы являются дочерними к управляемому CustomResource:
    kopf.append_owner_reference(persistent_volume_claim, owner=body)
    kopf.append_owner_reference(service, owner=body)
    kopf.append_owner_reference(deployment, owner=body)
    kopf.append_owner_reference(restore_job, owner=body)
    # ^ Таким образом при удалении CR удалятся все, связанные с ним pv, pvc, svc, deployments

    api = kubernetes.client.CoreV1Api()
    # Создаем mysql PV:
    # api.create_persistent_volume(persistent_volume)
    # Создаем mysql PVC:
    try:
        api.create_namespaced_persistent_volume_claim(
            'default', persistent_volume_claim)
        # Создаем mysql Deployment:
        api = kubernetes.client.AppsV1Api()
        api.create_namespaced_deployment('default', deployment)
        # Создаем mysql SVC:
        api = kubernetes.client.CoreV1Api()
        api.create_namespaced_service('default', service)
    except kubernetes.client.exceptions.ApiException as e:
        if e.status == 409:
            print("PVC already exists, skipping creation.")
        else:
            raise

    # Cоздаем PVC и PV для бэкапов:

    try:
        backup_pvc = render_template(
            'backup-pvc.yml.j2', {'name': name, 'storage_size': storage_size})
        api = kubernetes.client.CoreV1Api()
        api.create_namespaced_persistent_volume_claim('default', backup_pvc)
    except kubernetes.client.exceptions.ApiException as e:
        if e.status == 409:
            print("PVC already exists, skipping creation.")
        else:
            kopf.Logger.info(f'pvc creation error: {e}')
            raise

    try:
        api = kubernetes.client.BatchV1Api()
        api.create_namespaced_job('default', restore_job)
    except kubernetes.client.rest.ApiException:
        pass


@kopf.on.delete('otus.homework', 'v1', 'mysqls')
def delete_object_make_backup(body, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    password = body['spec']['password']
    database = body['spec']['database']

    delete_successful_jobs(name)
    # Cоздаем backup job:
    api = kubernetes.client.BatchV1Api()
    backup_job = render_template('backup-job.yml.j2', {
        'name': name,
        'image': image,
        'password': password,
        'database': database})
    api.create_namespaced_job('default', backup_job)
    wait_until_job_end(f'backup-{name}-job')
    kopf.info(body, reason='Delete',
              message='mysql and its children resources deleted')


@kopf.on.field('otus.homework', 'v1', 'mysqls', field='spec.password')
def update_object(body, diff, **kwargs):
    name = body['metadata']['name']
    image = body['spec']['image']
    database = body['spec']['database']
    delete_successful_jobs(name)
    print(f'password changed, diff: {diff}')
    for action, path, old_password, new_password in diff:
        if action == 'change':
            old_password = old_password if old_password else ''
            new_password = new_password  # noqa: F841
            break
        elif action == 'add':
            return
    else:
        kopf.info(body, reason='Update',
                  message='mysql password not changed')
        return
    # Cоздаем change password job:
    api = kubernetes.client.BatchV1Api()
    api.create_namespaced_job('default', render_template('change-password-job.yml.j2', {  # noqa: E501
        'name': name,
        'image': image,
        'old_password': old_password,
        'new_password': new_password,
        'database': database}))
    wait_until_job_end(f'change-password-{name}-job')
    kopf.info(body, reason='Update',
              message='mysql password updated')
