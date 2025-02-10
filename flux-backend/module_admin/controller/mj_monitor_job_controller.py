# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from typing import List
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_admin.aspect.data_scope import GetDataScope
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.annotation.log_annotation import Log
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response

from module_admin.entity.vo.mj_monitor_job_vo import MjMonitorJobPageModel, MjMonitorJobModel
from module_admin.service.mj_monitor_job_service import MjMonitorJobService

mjMonitorJobController = APIRouter(prefix='/mj/monitor', dependencies=[Depends(LoginService.get_current_user)])

@mjMonitorJobController.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('mj:monitor:list'))])
async def get_mj_monitor_job_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: MjMonitorJobPageModel = Depends( MjMonitorJobPageModel.as_query),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    mj_monitor_job_result = await MjMonitorJobService.get_mj_monitor_job_list(query_db, page_query, data_scope_sql)

    return ResponseUtil.success(model_content=mj_monitor_job_result)

@mjMonitorJobController.get('/getById/{mjMonitorJobId}', dependencies=[Depends(CheckUserInterfaceAuth('mj:monitor:list'))])
async def get_mj_monitor_job_by_id(
        request: Request,
        mjMonitorJobId: int,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    mj_monitor_job = await MjMonitorJobService.get_mj_monitor_job_by_id(query_db, mjMonitorJobId)
    return ResponseUtil.success(data=mj_monitor_job)


@mjMonitorJobController.post('/add', dependencies=[Depends(CheckUserInterfaceAuth('mj:monitor:add'))])
@Log(title='mj_monitor_job', business_type=BusinessType.INSERT)
async def add_mj_monitor_job (
    request: Request,
    add_model: MjMonitorJobModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await MjMonitorJobService.add_mj_monitor_job(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)

@mjMonitorJobController.put('/update', dependencies=[Depends(CheckUserInterfaceAuth('mj:monitor:update'))])
@Log(title='mj_monitor_job', business_type=BusinessType.UPDATE)
async def update_mj_monitor_job(
    request: Request,
    edit_model: MjMonitorJobModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await MjMonitorJobService.update_mj_monitor_job(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@mjMonitorJobController.delete('/delete/{mjMonitorJobIds}', dependencies=[Depends(CheckUserInterfaceAuth('mj:monitor:del'))])
@Log(title='mj_monitor_job', business_type=BusinessType.DELETE)
async def del_mj_monitor_job(
    request: Request,
    mjMonitorJobIds: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    ids = mjMonitorJobIds.split(',')
    del_result = await MjMonitorJobService.del_mj_monitor_job(query_db, ids)
    return ResponseUtil.success(data=del_result)

@mjMonitorJobController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('mj:monitor:export'))])
@Log(title='mj_monitor_job', business_type=BusinessType.EXPORT)
async def export_mj_monitor_job(
    request: Request,
    mj_monitor_job_form: MjMonitorJobPageModel = Form(),
    query_db: AsyncSession = Depends(get_db),
    data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    # 获取全量数据
    export_result = await MjMonitorJobService.export_mj_monitor_job_list(
        query_db, mj_monitor_job_form, data_scope_sql
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))