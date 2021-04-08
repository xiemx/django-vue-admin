import request from '@/utils/request'

export function namespaces(cluster) {
  return request({
    url: '/k8s/namespace/',
    method: 'get',
    params: { cluster }
  })
}
