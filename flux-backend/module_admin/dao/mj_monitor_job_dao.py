# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.mj_monitor_job_do import MjMonitorJob
from module_admin.entity.vo.mj_monitor_job_vo import MjMonitorJobPageModel, MjMonitorJobModel
from utils.page_util import PageUtil, PageResponseModel


class MjMonitorJobDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, mj_monitor_job_id: int) -> MjMonitorJob:
        """根据主键获取单条记录"""
        mj_monitor_job = (((await db.execute(
                            select(MjMonitorJob)
                            .where(MjMonitorJob.id == mj_monitor_job_id)))
                       .scalars())
                       .first())
        return mj_monitor_job

    """
    查询
    """
    @classmethod
    async def get_mj_monitor_job_list(cls, db: AsyncSession,
                             query_object: MjMonitorJobPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(MjMonitorJob)
            .where(
                MjMonitorJob.create_source == query_object.create_source if query_object.create_source else True,
                MjMonitorJob.current_status == query_object.current_status if query_object.current_status else True,
                MjMonitorJob.discord_url.like(f"%{query_object.discord_url}%") if query_object.discord_url else True,
                MjMonitorJob.enqueue_time.between(query_object.begin_enqueue_time, query_object.end_enqueue_time) if query_object.enqueue_time else True,
                MjMonitorJob.event_type == query_object.event_type if query_object.event_type else True,
                MjMonitorJob.full_command.like(f"%{query_object.full_command}%") if query_object.full_command else True,
                MjMonitorJob.job_id == query_object.job_id if query_object.job_id else True,
                MjMonitorJob.job_type == query_object.job_type if query_object.job_type else True,
                MjMonitorJob.mj_id == query_object.mj_id if query_object.mj_id else True,
                MjMonitorJob.username == query_object.username if query_object.username else True,
                MjMonitorJob.user_id == query_object.user_id if query_object.user_id else True,
                MjMonitorJob.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(MjMonitorJob.create_time))
            .distinct()
        )
        mj_monitor_job_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return mj_monitor_job_list


    @classmethod
    async def add_mj_monitor_job(cls, db: AsyncSession, add_model: MjMonitorJobModel, auto_commit: bool = True) -> MjMonitorJob:
        """
        增加
        """
        mj_monitor_job =  MjMonitorJob(**add_model.model_dump(exclude_unset=True))
        db.add(mj_monitor_job)
        await db.flush()
        if auto_commit:
            await db.commit()
        return mj_monitor_job

    @classmethod
    async def edit_mj_monitor_job(cls, db: AsyncSession, edit_model: MjMonitorJobModel, auto_commit: bool = True) -> MjMonitorJob:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(MjMonitorJob), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_mj_monitor_job(cls, db: AsyncSession, mj_monitor_job_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(MjMonitorJob).where(MjMonitorJob.id.in_(mj_monitor_job_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(MjMonitorJob).where(MjMonitorJob.id.in_(mj_monitor_job_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()