from celery import shared_task
from toolkit.models import toolKitExam, toolKitIngressWhitelist, toolKitKubernetesCleaner, toolKitAutoScaling, toolKitGraphiteCleaner
from django.utils import timezone as datetime
import requests
import re
import time
import os
from django.contrib.auth.models import User
from tempfile import NamedTemporaryFile
from kubernetes import client, config
from k8s.models import KubernetesCluster, KubernetesNamespace
from django.conf import settings
from toolkit.utils import trigger_pipeline
from common.notice import dingding
from common.callback import Callback
import codecs
import sys
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkram.request.v20150501.ListUsersRequest import ListUsersRequest

access_token = settings.GITLAB_ACCESS_KEY


@shared_task
def toolkit_create_exam(task_id=None, **kwargs):

    if task_id is None:
        user = User.objects.get_or_create(username="scheduler")[0]
        exam = toolKitExam(
            user=user, status="RUNNING", task_id=toolkit_create_exam.request.id)
    else:
        exam = toolKitExam.objects.get(id=task_id)
        exam.status = "RUNNING"
        exam.task_id = toolkit_create_exam.request.id
        dingding.send(title=exam.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          exam.status.upper(),
                          exam.user.profile.phone,
                          'toolkit_create_exam',
                          exam.id,
                          exam.task_id),
                      users=[exam.user.profile.phone]
                      )
    try:
        exam.save()

        project_id = settings.EXAM_PROJECT_ID
        trigger_token = settings.EXAM_TRIGGER_TOKEN
        ref = settings.EXAM_TRIGGER_REF
        job_name = settings.EXAM_JOB_NAME

        pipeline = trigger_pipeline(project_id, trigger_token, ref, **kwargs)

        while pipeline.finished_at is None:
            pipeline.refresh()
            time.sleep(60)

        if pipeline.status != "success":
            raise Exception(
                "create exam failed, pipeline status is {}.".format(pipeline.status))

        project = pipeline.manager.gitlab.projects.get(project_id)

        for job in pipeline.jobs.list():

            if job.name == job_name:
                log = project.jobs.get(job.id).trace().decode()
                id = re.findall('测评 ID[:：](.*)', log)
                url = re.findall('测评地址[:：](.*)', log)

                if not id or not url:
                    raise Exception(
                        'check regex, exam_id or exam_url is null! log: {}'.format(log))

                exam.exam_id, exam.exam_url, exam.status = id[0].strip(
                ), url[0].strip(), "SUCCESS"
                exam.save()

    except Exception as err:
        exam.status = "FAILURE"
        exam.save()
        dingding.send(title=exam.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          exam.status.upper(),
                          exam.user.profile.phone,
                          'toolkit_create_exam',
                          exam.id,
                          exam.task_id),
                      users=[exam.user.profile.phone]
                      )
        raise Exception(err)
    else:
        dingding.send(title=exam.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          exam.status.upper(),
                          exam.user.profile.phone,
                          'toolkit_create_exam',
                          exam.id,
                          exam.task_id),
                      users=[exam.user.profile.phone]
                      )
        return "exam id: {}, exam url: {}".format(exam.exam_id, exam.exam_url)


@shared_task
def toolkit_update_ingress_whitelist(task_id=None, **kwargs):

    if task_id is None:
        user = User.objects.get_or_create(username="scheduler")[0]
        whitelist = toolKitIngressWhitelist(
            user=user, status="RUNNING", task_id=toolkit_update_ingress_whitelist.request.id)
    else:
        whitelist = toolKitIngressWhitelist.objects.get(id=task_id)
        whitelist.status = "RUNNING"
        whitelist.task_id = toolkit_update_ingress_whitelist.request.id
        dingding.send(title=whitelist.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          whitelist.status.upper(),
                          whitelist.user.profile.phone,
                          'toolkit_update_ingress_whitelist',
                          whitelist.id,
                          whitelist.task_id),
                      users=[whitelist.user.profile.phone]
                      )

    try:
        whitelist.save()

        project_id = settings.INGRESS_PROJECT_ID
        trigger_token = settings.INGRESS_TRIGGER_TOKEN
        ref = settings.INGRESS_TRIGGER_REF
        job_name = settings.INGRESS_JOB_NAME

        kwargs['ACTION'] = 'ingress_whitelist'

        pipeline = trigger_pipeline(project_id, trigger_token, ref, **kwargs)
        while pipeline.finished_at is None:
            pipeline.refresh()
            time.sleep(60)

        if pipeline.status != "success":
            raise Exception(
                "update ingress whitelist failed, pipeline status is {}.".format(pipeline.status))

        whitelist.status = "SUCCESS"
        whitelist.save()

    except Exception as err:
        whitelist.status = "FAILURE"
        whitelist.save()
        dingding.send(title=whitelist.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          whitelist.status.upper(),
                          whitelist.user.profile.phone,
                          'toolkit_update_ingress_whitelist',
                          whitelist.id,
                          whitelist.task_id),
                      users=[whitelist.user.profile.phone]
                      )
        raise Exception(err)

    else:
        dingding.send(title=whitelist.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          whitelist.status.upper(),
                          whitelist.user.profile.phone,
                          'toolkit_update_ingress_whitelist',
                          whitelist.id,
                          whitelist.task_id),
                      users=[whitelist.user.profile.phone]
                      )
        return "update ingress whitelist success."


@shared_task
def toolkit_clean_evicted_pod(cluster, task_id=None):

    cluster = KubernetesCluster.objects.get(name=cluster)

    if task_id is None:
        user = User.objects.get_or_create(username="scheduler")[0]
        cleaner = toolKitKubernetesCleaner(
            user=user, status="RUNNING", cluster=cluster, task_id=toolkit_clean_evicted_pod.request.id)
    else:
        cleaner = toolKitKubernetesCleaner.objects.get(id=task_id)
        cleaner.status = "RUNNING"
        cleaner.task_id = toolkit_clean_evicted_pod.request.id
        dingding.send(title=cleaner.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          cleaner.status.upper(),
                          cleaner.user.profile.phone,
                          'toolkit_clean_evicted_pod',
                          cleaner.id,
                          cleaner.task_id),
                      users=[cleaner.user.profile.phone]
                      )

    try:
        cleaner.save()

        client = KubernetesNamespace.get_client(cluster_config=cluster.config)
        v1 = client.AppsV1Api()
        coreV1 = client.CoreV1Api()

        pods = coreV1.list_pod_for_all_namespaces().items
        __pod_list = []
        for pod in pods:
            if pod.status.phase == "Failed" and pod.status.reason == "Evicted":

                namespace = pod.metadata.namespace
                pod = pod.metadata.name
                body = client.V1beta1Eviction(
                    metadata=client.V1ObjectMeta(name=pod, namespace=namespace))
                response = coreV1.create_namespaced_pod_eviction(
                    name=pod, namespace=namespace, body=body, pretty=True)
                __pod_list.append("{}/{}".format(namespace, pod))

    except Exception as err:
        cleaner.status = "FAILURE"
        cleaner.save()
        dingding.send(title=cleaner.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          cleaner.status.upper(),
                          cleaner.user.profile.phone,
                          'toolkit_clean_evicted_pod',
                          cleaner.id,
                          cleaner.task_id),
                      users=[cleaner.user.profile.phone]
                      )
        raise Exception(err)

    else:
        cleaner.status = "SUCCESS"
        cleaner.pods = __pod_list
        cleaner.save()
        dingding.send(title=cleaner.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          cleaner.status.upper(),
                          cleaner.user.profile.phone,
                          'toolkit_clean_evicted_pod',
                          cleaner.id,
                          cleaner.task_id),
                      users=[cleaner.user.profile.phone]
                      )
        return "Pod: {} is evicted!".format(__pod_list)


@shared_task
def toolkit_autoscaling_service(task_id=None, **kwargs):

    __services = settings.SERVICES_MAP

    if task_id is None:
        service_name = kwargs.get("service_name", None)
        number = kwargs.get("number", None)
        namespace = kwargs.get("namespace", None)
        if not service_name or not number:
            raise Exception(
                "parameters error, variable service: {} or number: {} is not found.".format(service_name, number))

        user = User.objects.get_or_create(username="scheduler")[0]
        scaler = toolKitAutoScaling(
            user=user, status="RUNNING", service=service_name, namespace=namespace, number=number, task_id=toolkit_autoscaling_service.request.id)
        scaler.save()
    else:
        scaler = toolKitAutoScaling.objects.get(id=task_id)
        scaler.status = "RUNNING"
        scaler.task_id = toolkit_autoscaling_service.request.id
        scaler.save()
        dingding.send(title=scaler.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          scaler.status.upper(),
                          scaler.user.profile.phone,
                          'toolkit_autoscaling_service',
                          scaler.id,
                          scaler.task_id),
                      users=[scaler.user.profile.phone]
                      )

        service_name = scaler.service

    service = __services.get(service_name)

    try:
        project_id = service.get("project_id")
        trigger_token = service.get("trigger_token")
        ref = service.get("ref", "master")

        if "SERVICE_NAME" not in kwargs.keys():
            kwargs["SERVICE_NAME"] = scaler.service

        if "NUMBER" not in kwargs.keys():
            kwargs["NUMBER"] = str(scaler.number)

        if "NAMESPACE" not in kwargs.keys() and scaler.namespace is not None:
            kwargs["NAMESPACE"] = scaler.namespace

        pipeline = trigger_pipeline(project_id, trigger_token, ref, **kwargs)

        while pipeline.finished_at is None:
            pipeline.refresh()
            time.sleep(60)

        if pipeline.status != "success":
            raise Exception(
                "update ingress whitelist failed, pipeline status is {}.".format(pipeline.status))

        scaler.status = "SUCCESS"
        scaler.save()

    except Exception as err:
        scaler.status = "FAILURE"
        scaler.save()
        dingding.send(title=scaler.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          scaler.status.upper(),
                          scaler.user.profile.phone,
                          'toolkit_autoscaling_service',
                          scaler.id,
                          scaler.task_id),
                      users=[scaler.user.profile.phone]
                      )
        raise Exception(err)

    else:
        dingding.send(title=scaler.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          scaler.status.upper(),
                          scaler.user.profile.phone,
                          'toolkit_autoscaling_service',
                          scaler.id,
                          scaler.task_id),
                      users=[scaler.user.profile.phone]
                      )
        return "service sacling success."


@shared_task
def toolkit_graphite_cleaner(task_id=None, **kwargs):

    if task_id is None:
        user = User.objects.get_or_create(username="scheduler")[0]
        cleaner = toolKitGraphiteCleaner(
            user=user, status="RUNNING", task_id=toolkit_graphite_cleaner.request.id)
    else:
        cleaner = toolKitGraphiteCleaner.objects.get(id=task_id)
        cleaner.status = "RUNNING"
        cleaner.task_id = toolkit_graphite_cleaner.request.id
        dingding.send(title=cleaner.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          cleaner.status.upper(),
                          cleaner.user.profile.phone,
                          'toolkit_graphite_cleaner',
                          cleaner.id,
                          cleaner.task_id),
                      users=[cleaner.user.profile.phone]
                      )

    try:
        # 更新任务状态为RUNNING
        cleaner.save()

        project_id = settings.GRAPHITE_PROJECT_ID
        trigger_token = settings.GRAPHITE_TRIGGER_TOKEN
        ref = settings.GRAPHITE_TRIGGER_REF

        # if 'ACTION' not in kwargs.keys() or kwargs.get("ACTION") != '':
        kwargs['ACTION'] = 'clean_graphite_storage'

        pipeline = trigger_pipeline(project_id, trigger_token, ref, **kwargs)
        while pipeline.finished_at is None:
            pipeline.refresh()
            time.sleep(60)

        if pipeline.status != "success":
            raise Exception(
                "update ingress whitelist failed, pipeline status is {}.".format(pipeline.status))

        cleaner.status = "SUCCESS"
        cleaner.save()

    except Exception as err:
        cleaner.status = "FAILURE"
        cleaner.save()
        dingding.send(title=cleaner.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          cleaner.status.upper(),
                          cleaner.user.profile.phone,
                          'toolkit_graphite_cleaner',
                          cleaner.id,
                          cleaner.task_id),
                      users=[cleaner.user.profile.phone])

        raise Exception(err)

    else:
        dingding.send(title=cleaner.status,
                      content="### **{}** @{} \n > * TASK: {}\n > * ID: {} \n > * TASK_ID: {}".format(
                          cleaner.status.upper(),
                          cleaner.user.profile.phone,
                          'toolkit_graphite_cleaner',
                          cleaner.id,
                          cleaner.task_id),
                      users=[cleaner.user.profile.phone]
                      )
        return "Successfully cleaned up storage space."


@shared_task(base=Callback)
def update_alicloud_uid(*args, **kwargs):

    sk = settings.ALICLOUD_SECRET_KEY
    ak = settings.ALICLOUD_ACCESS_KEY
    region = settings.ALICLOUD_REGION

    ali_client = AcsClient(ak, sk, region)

    request = ListUsersRequest()
    request.set_accept_format('json')
    response = ali_client.do_action_with_exception(request)

    for u in json.loads(response).get('Users').get('User'):
        user = User.objects.filter(username=u.get('UserName')).first()
        if user:
            user.profile.alicloud = u.get("UserId")
            user.profile.save()

    return "update success!"
