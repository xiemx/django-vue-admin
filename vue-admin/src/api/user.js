import request from '@/utils/request'
import VueJwtDecode from 'vue-jwt-decode'

export function login(data) {
  return request({
    url: '/user/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  var url = "/user/" + VueJwtDecode.decode(token)["user_id"]
  return request({
    url,
    method: 'get',
    // params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout/',
    method: 'post'
  })
}

export function users() {
  return request({
    url: '/user/',
    method: 'get'
  })
}

export function editUser(data) {
  return request({
    url: '/user/' + data.id + '/',
    method: 'patch',
    data
  })
}
