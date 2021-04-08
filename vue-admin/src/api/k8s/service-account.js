import request from '@/utils/request'

export function serviceAccounts(cluster, namespace) {
  return request({
    url: '/k8s/service-account/',
    method: 'get',
    params: { cluster, namespace }
  })
}
