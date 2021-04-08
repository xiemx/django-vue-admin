import request from '@/utils/request'

export function daemonsets(cluster, namespace) {
  return request({
    url: '/k8s/daemonset/',
    method: 'get',
    params: { cluster, namespace }
  })
}
