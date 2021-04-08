import request from '@/utils/request'

export function list() {
  return request({
    url: '/job/solar/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/job/solar/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/job/solar/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/job/solar/' + data.id + '/',
    method: 'delete',
    data
  })
}

