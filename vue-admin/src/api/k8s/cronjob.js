import request from '@/utils/request'

export function cronjobs(cluster, namespace) {
  return request({
    url: '/k8s/cronjob/',
    method: 'get',
    params: { cluster, namespace }
  })
}
