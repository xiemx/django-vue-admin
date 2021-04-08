import request from '@/utils/request'

export function deployments(cluster, namespace) {
  return request({
    url: '/k8s/deployment/',
    method: 'get',
    params: { cluster, namespace }
  })
}
