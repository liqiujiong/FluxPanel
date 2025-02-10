import request from '@/utils/request'

// 查询mj监控任务列表列表
export function listMonitor(query) {
  return request({
    url: '/mj/monitor/list',
    method: 'get',
    params: query
  })
}

// 查询mj监控任务列表详细
export function getMonitor(id) {
  return request({
    url: '/mj/monitor/getById/' + id,
    method: 'get'
  })
}

// 新增mj监控任务列表
export function addMonitor(data) {
  return request({
    url: '/mj/monitor/add',
    method: 'post',
    data: data
  })
}

// 修改mj监控任务列表
export function updateMonitor(data) {
  return request({
    url: '/mj/monitor/update',
    method: 'put',
    data: data
  })
}

// 删除mj监控任务列表
export function delMonitor(id) {
  return request({
    url: '/mj/monitor/delete/' + id,
    method: 'delete'
  })
}