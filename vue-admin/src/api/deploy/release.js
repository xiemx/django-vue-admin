import request from '@/utils/request'

export function list(kwargs) {
  console.log(kwargs)
  var limit = kwargs.limit
  var offset = kwargs.offset
  var user = kwargs.user
  var cluster = kwargs.cluster
  var type = kwargs.type
  var namespace = kwargs.namespace
  var service = kwargs.service
  var task_id = kwargs.task_id
  var time_range = kwargs.time_range

  return request({
    url: '/deploy/release/',
    method: 'get',
    params: { limit, offset, cluster, type, user, namespace, service, task_id, time_range }
  })
}

export function create(data) {
  return request({
    url: '/deploy/release/',
    method: 'post',
    data
  })
}

export function update(data) {
  return request({
    url: '/deploy/release/' + data.id + '/',
    method: 'patch',
    data
  })
}

export function deleted(data) {
  return request({
    url: '/deploy/release/' + data.id + '/',
    method: 'delete',
    data
  })
}

