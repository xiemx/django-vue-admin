import request from '@/utils/request'

export function clusters() {
  return request({
    url: '/k8s/cluster/',
    method: 'get',
    // params
  })
}
