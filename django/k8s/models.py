# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from tempfile import NamedTemporaryFile
from kubernetes import client, config
import json


class KubernetesBaseModel(models.Model):
    """
    base model
    """
    class Meta:
        abstract = True

    name_validator = UnicodeUsernameValidator()

    name = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[name_validator],
        error_messages={
            'unique': "resource already exists.",
        },
    )
    labels = models.CharField(max_length=1000, blank=True)
    annotations = models.CharField(max_length=3000, blank=True)
    create_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=150, blank=True)

    @classmethod
    def get_client(cls, cluster_config, API=client.CoreV1Api, **kwargs):
        """
        Gets a k8s api client
        """

        with NamedTemporaryFile() as ntf:
            kwargs["config_file"] = ntf.name
            cc = json.dumps(cluster_config) if isinstance(
                cluster_config, dict) else cluster_config

            with open(ntf.name, "w") as f:
                f.write(cc)

            config.load_kube_config(ntf.name)
            configuration = client.Configuration.get_default_copy()
            configuration.verify_ssl = False
            client.Configuration.set_default(configuration)

            return client


class KubernetesCluster(models.Model):
    """
    Cluster Model
    """

    name_validator = UnicodeUsernameValidator()

    name = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[name_validator],
        error_messages={
            'unique': "resource already exists.",
        },
    )

    description = models.CharField(max_length=150, blank=True)
    displayname = models.CharField(
        max_length=150,
        validators=[name_validator],
        blank=True
    )

    api_endpoint = models.URLField(help_text="Cluster Endpoint URL")
    config = JSONField(help_text="Equivalent to .kube/config but all JSON",
                       null=True,
                       )
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)


class KubernetesNamespace(KubernetesBaseModel):
    """
    NameSpace Model
    """
    class Meta:
        abstract = False


class KubernetesDeployment(KubernetesBaseModel):
    """
    NameSpace Model
    """
    class Meta:
        abstract = False
