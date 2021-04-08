import request from '@/utils/request'

export function services(cluster, namespace) {
  return request({
    url: '/k8s/service/',
    method: 'get',
    params: { cluster, namespace }
  })
}
