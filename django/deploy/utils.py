
from k8s.models import KubernetesCluster
from tempfile import NamedTemporaryFile
import subprocess
import json


def exec_helm_command(cluster, command):
    _cluster = KubernetesCluster.objects.get(name=cluster)

    with NamedTemporaryFile() as ntf:
        cc = json.dumps(_cluster.config)
        with open(ntf.name, "w") as f:
            f.write(cc)

        cmd = command + " --kubeconfig {}".format(ntf.name)

        return subprocess.getstatusoutput(cmd)
