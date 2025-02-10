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

from module_admin.entity.vo.mj_account_vo import MjAccountPageModel, MjAccountModel
from module_admin.service.mj_account_service import MjAccountService

mjAccountController = APIRouter(prefix='/mj/account', dependencies=[Depends(LoginService.get_current_user)])


@mjAccountController.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('mj:account:list'))])
async def get_mj_account_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: MjAccountPageModel = Depends( MjAccountPageModel.as_query),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    mj_account_result = await MjAccountService.get_mj_account_list(query_db, page_query, data_scope_sql)

    return ResponseUtil.success(model_content=mj_account_result)

@mjAccountController.get('/getById/{mjAccountId}', dependencies=[Depends(CheckUserInterfaceAuth('mj:account:list'))])
async def get_mj_account_by_id(
        request: Request,
        mjAccountId: int,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    mj_account = await MjAccountService.get_mj_account_by_id(query_db, mjAccountId)
    return ResponseUtil.success(data=mj_account)


@mjAccountController.post('/add', dependencies=[Depends(CheckUserInterfaceAuth('mj:account:add'))])
@Log(title='mj_account', business_type=BusinessType.INSERT)
async def add_mj_account (
    request: Request,
    add_model: MjAccountModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await MjAccountService.add_mj_account(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)

@mjAccountController.put('/update', dependencies=[Depends(CheckUserInterfaceAuth('mj:account:update'))])
@Log(title='mj_account', business_type=BusinessType.UPDATE)
async def update_mj_account(
    request: Request,
    edit_model: MjAccountModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await MjAccountService.update_mj_account(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@mjAccountController.delete('/delete/{mjAccountIds}', dependencies=[Depends(CheckUserInterfaceAuth('mj:account:del'))])
@Log(title='mj_account', business_type=BusinessType.DELETE)
async def del_mj_account(
    request: Request,
    mjAccountIds: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    ids = mjAccountIds.split(',')
    del_result = await MjAccountService.del_mj_account(query_db, ids)
    return ResponseUtil.success(data=del_result)

@mjAccountController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('mj:account:export'))])
@Log(title='mj_account', business_type=BusinessType.EXPORT)
async def export_mj_account(
    request: Request,
    mj_account_form: MjAccountPageModel = Form(),
    query_db: AsyncSession = Depends(get_db),
    data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    # 获取全量数据
    export_result = await MjAccountService.export_mj_account_list(
        query_db, mj_account_form, data_scope_sql
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))