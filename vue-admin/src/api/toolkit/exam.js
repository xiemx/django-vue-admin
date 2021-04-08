import request from '@/utils/request'

export function list() {
  return request({
    url: '/toolkit/exam/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/toolkit/exam/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/toolkit/exam/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/toolkit/exam/' + data.id + '/',
    method: 'delete',
    data
  })
}

