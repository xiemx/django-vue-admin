import request from '@/utils/request'

export function list() {
  return request({
    url: '/job/crontab/',
    method: 'get'
  })
}

export function create(data) {
  return request({
    url: '/job/crontab/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/job/crontab/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/job/crontab/' + data.id + '/',
    method: 'delete',
    data
  })
}

