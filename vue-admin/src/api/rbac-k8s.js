import request from '@/utils/request'

export function k8sRBAC(cluster) {
  return request({
    url: '/rbac-k8s/',
    method: 'get',
    params: { cluster }
  })
}
