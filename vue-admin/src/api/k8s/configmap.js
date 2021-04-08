import request from '@/utils/request'

export function configmaps(cluster, namespace) {
  return request({
    url: '/k8s/configmap/',
    method: 'get',
    params: { cluster, namespace }
  })
}
