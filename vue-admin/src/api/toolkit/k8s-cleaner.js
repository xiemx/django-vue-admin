import request from '@/utils/request'

export function list(kwargs) {
  var limit = kwargs.limit
  var offset = kwargs.offset
  return request({
    url: 'toolkit/k8s-cleaner/',
    method: 'get',
    params: { limit, offset }
  })
}

export function create(data) {
  return request({
    url: '/toolkit/k8s-cleaner/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/toolkit/k8s-cleaner/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/toolkit/k8s-cleaner/' + data.id + '/',
    method: 'delete',
    data
  })
}

