import request from '@/utils/request'

export function list() {
  return request({
    url: '/job/interval/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/job/interval/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/job/interval/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/job/interval/' + data.id + '/',
    method: 'delete',
    data
  })
}

