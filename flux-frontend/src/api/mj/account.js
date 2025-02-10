import request from '@/utils/request'

// 查询mj账号列表
export function listAccount(query) {
  return request({
    url: '/mj/account/list',
    method: 'get',
    params: query
  })
}

// 查询mj账号详细
export function getAccount(id) {
  return request({
    url: '/mj/account/getById/' + id,
    method: 'get'
  })
}

// 新增mj账号
export function addAccount(data) {
  return request({
    url: '/mj/account/add',
    method: 'post',
    data: data
  })
}

// 修改mj账号
export function updateAccount(data) {
  return request({
    url: '/mj/account/update',
    method: 'put',
    data: data
  })
}

// 删除mj账号
export function delAccount(id) {
  return request({
    url: '/mj/account/delete/' + id,
    method: 'delete'
  })
}