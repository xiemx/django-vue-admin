import request from '@/utils/request'

export function list(cluster, namespace) {
  return request({
    url: '/k8s/ingress/',
    method: 'get',
    params: { cluster, namespace }
  })
}
