import request from '@/utils/request'

export function groups() {
  return request({
    url: '/group/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/group/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/group/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/group/' + data.id + '/',
    method: 'delete',
    data
  })
}

