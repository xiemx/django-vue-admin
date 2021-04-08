import request from '@/utils/request'

export function list() {
  return request({
    url: '/job/clocked/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/job/clocked/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/job/clocked/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/job/clocked/' + data.id + '/',
    method: 'delete',
    data
  })
}

