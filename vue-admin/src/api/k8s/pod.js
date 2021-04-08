import request from '@/utils/request'

export function pods(cluster, namespace) {
  return request({
    url: '/k8s/pod/',
    method: 'get',
    params: { cluster, namespace }
  })
}
