import request from '@/utils/request'

export function list(kwargs) {
  var limit = kwargs.limit
  var offset = kwargs.offset
  return request({
    url: '/toolkit/ingress-whitelist/',
    method: 'get',
    params: { limit, offset }
  })
}

export function create(data) {
  return request({
    url: '/toolkit/ingress-whitelist/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/toolkit/ingress-whitelist/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/toolkit/ingress-whitelist/' + data.id + '/',
    method: 'delete',
    data
  })
}

