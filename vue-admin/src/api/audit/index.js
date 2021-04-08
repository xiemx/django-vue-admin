import request from '@/utils/request'

export function list(kwargs) {
  var limit = kwargs.limit
  var offset = kwargs.offset
  var resource = kwargs.resource
  var operation = kwargs.operation
  var username = kwargs.username
  var time_range = kwargs.time_range
  return request({
    url: '/audit/operation/',
    method: 'get',
    params: { limit, offset, username, resource, operation, time_range }
  })
}
