import request from '@/utils/request'

export function secrets(cluster, namespace) {
  return request({
    url: '/k8s/secret/',
    method: 'get',
    params: { cluster, namespace }
  })
}
