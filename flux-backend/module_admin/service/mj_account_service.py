# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from module_admin.dao.mj_account_dao import MjAccountDao
from module_admin.entity.do.mj_account_do import MjAccount
from module_admin.entity.vo.mj_account_vo import MjAccountPageModel, MjAccountModel


class MjAccountService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_mj_account_list(cls, query_db: AsyncSession, query_object: MjAccountPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        mj_account_list = await MjAccountDao.get_mj_account_list(query_db, query_object, data_scope_sql, is_page=True)
        return mj_account_list

    @classmethod
    async def get_mj_account_by_id(cls, query_db: AsyncSession, mj_account_id: int) -> MjAccountModel:
        mj_account = await  MjAccountDao.get_by_id(query_db, mj_account_id)
        mj_account_model = MjAccountModel(**CamelCaseUtil.transform_result(mj_account))
        return mj_account_model


    @classmethod
    async def add_mj_account(cls, query_db: AsyncSession, query_object: MjAccountModel) -> MjAccountModel:
        mj_account = await MjAccountDao.add_mj_account(query_db, query_object)
        mj_account_model = MjAccountModel(**CamelCaseUtil.transform_result(mj_account))
        return mj_account_model


    @classmethod
    async def update_mj_account(cls, query_db: AsyncSession, query_object: MjAccountModel) -> MjAccountModel:
        mj_account = await MjAccountDao.edit_mj_account(query_db, query_object)
        mj_account_model = MjAccountModel(**CamelCaseUtil.transform_result(mj_account))
        return mj_account_model


    @classmethod
    async def del_mj_account(cls, query_db: AsyncSession, mj_account_ids: List[str]):
        await MjAccountDao.del_mj_account(query_db, mj_account_ids)


    @classmethod
    async def export_mj_account_list(cls, query_db: AsyncSession, query_object: MjAccountPageModel, data_scope_sql) -> bytes:
        mj_account_list = await MjAccountDao.get_mj_account_list(query_db, query_object, data_scope_sql, is_page=False)
        mapping_dict = {
            'email': '邮箱 ',
            'errorMsg': '异常信息 ',
            'lastMonitorTime': '监控时间 ',
            'mjId': 'mj_id ',
            'monitorStatus': '监控状态 ',
            'plan': '订阅计划 ',
            'remark': '备注 ',
            'status': '订阅状态 ',
            'subscribeTime': '开通时间 ',
            'totalJobs': '总出图数 ',
            'updateTime': '更新时间 ',
        }
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in mj_account_list
        ]
        binary_data = export_list2excel(new_data)
        return binary_data
    
class MjAccountInstance:
    """
    账号实例
    """
    def __init__(self, mj_account: MjAccountModel):
        self.mj_account = mj_account
        self.mj_site_api = MjSiteApi(
            mj_user_id=mj_account.user_id,
            mj_site_cookie=mj_account.cookie
        )

    async def update_mj_account_baseinfo(self):
        # 通过mj_site_api获取账号信息进行更新
        if not self.mj_site_api.mj_user_id:
            await self.mj_site_api.get_users_queue()
        pass

    async def fetch_mj_account_baseinfo(self):
        if not self.mj_site_api.mj_user_id:
            await self.mj_site_api.get_users_queue()
        pass
