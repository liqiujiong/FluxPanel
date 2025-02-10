# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.mj_account_do import MjAccount
from module_admin.entity.vo.mj_account_vo import MjAccountPageModel, MjAccountModel
from utils.page_util import PageUtil, PageResponseModel


class MjAccountDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, mj_account_id: int) -> MjAccount:
        """根据主键获取单条记录"""
        mj_account = (((await db.execute(
                            select(MjAccount)
                            .where(MjAccount.id == mj_account_id)))
                       .scalars())
                       .first())
        return mj_account

    """
    查询
    """
    @classmethod
    async def get_mj_account_list(cls, db: AsyncSession,
                             query_object: MjAccountPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(MjAccount)
            .where(
                MjAccount.email.like(f"%{query_object.email}%") if query_object.email else True,
                MjAccount.mj_id == query_object.mj_id if query_object.mj_id else True,
                MjAccount.monitor_status == query_object.monitor_status if query_object.monitor_status else True,
                MjAccount.plan == query_object.plan if query_object.plan else True,
                MjAccount.status == query_object.status if query_object.status else True,
                MjAccount.subscribe_time.between(query_object.begin_subscribe_time, query_object.end_subscribe_time) if query_object.subscribe_time else True,
                MjAccount.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(MjAccount.create_time))
            .distinct()
        )
        mj_account_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return mj_account_list


    @classmethod
    async def add_mj_account(cls, db: AsyncSession, add_model: MjAccountModel, auto_commit: bool = True) -> MjAccount:
        """
        增加
        """
        mj_account =  MjAccount(**add_model.model_dump(exclude_unset=True))
        db.add(mj_account)
        await db.flush()
        if auto_commit:
            await db.commit()
        return mj_account

    @classmethod
    async def edit_mj_account(cls, db: AsyncSession, edit_model: MjAccountModel, auto_commit: bool = True) -> MjAccount:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(MjAccount), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_mj_account(cls, db: AsyncSession, mj_account_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(MjAccount).where(MjAccount.id.in_(mj_account_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(MjAccount).where(MjAccount.id.in_(mj_account_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()