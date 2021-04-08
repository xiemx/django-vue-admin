import request from '@/utils/request'

export function roles(cluster, namespace) {
  return request({
    url: '/k8s/role/',
    method: 'get',
    params: { cluster, namespace }
  })
}
