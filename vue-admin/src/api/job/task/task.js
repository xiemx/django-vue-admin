import request from '@/utils/request'

export function list() {
  return request({
    url: '/job/task/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/job/task/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/job/task/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/job/task/' + data.id + '/',
    method: 'delete',
    data
  })
}

