import request from '@/utils/request'

export function clusterRoleBindings(cluster) {
  return request({
    url: '/k8s/cluster-role-binding/',
    method: 'get',
    params: { cluster }
  })
}
