import request from '@/utils/request'

export function statefulsets(cluster, namespace) {
  return request({
    url: '/k8s/statefulset/',
    method: 'get',
    params: { cluster, namespace }
  })
}
