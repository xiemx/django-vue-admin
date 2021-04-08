import request from '@/utils/request'

export function jobs(cluster, namespace) {
  return request({
    url: '/k8s/job/',
    method: 'get',
    params: { cluster, namespace }
  })
}
