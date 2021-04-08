import request from '@/utils/request'

export function permissions() {
  var url = "/permission/"
  return request({
    url,
    method: 'get',
  })
}
