import request from '@/utils/request'

export function clusterRoles(cluster) {
  return request({
    url: '/k8s/cluster-role/',
    method: 'get',
    params: { cluster }
  })
}
