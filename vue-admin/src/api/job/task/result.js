import request from '@/utils/request'

export function list(kwargs) {
  var limit = kwargs.limit
  var offset = kwargs.offset
  var task_id = kwargs.task_id
  var name = kwargs.name
  var time_range = kwargs.time_range
  return request({
    url: '/job/task_result/',
    method: 'get',
    params: { limit, offset, task_id, name, time_range }
  })
}
