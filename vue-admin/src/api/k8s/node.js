import request from '@/utils/request'

export function nodes(cluster) {
  return request({
    url: '/k8s/node/',
    method: 'get',
    params: { cluster }
  })
}
