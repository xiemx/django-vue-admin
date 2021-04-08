import request from '@/utils/request'

export function roleBindings(cluster, namespace) {
  return request({
    url: '/k8s/role-binding/',
    method: 'get',
    params: { cluster, namespace }
  })
}
