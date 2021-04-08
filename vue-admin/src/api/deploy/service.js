import request from '@/utils/request'

export function list() {
  return request({
    url: '/deploy/service/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/deploy/service/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/deploy/service/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/deploy/service/' + data.id + '/',
    method: 'delete',
    data
  })
}

