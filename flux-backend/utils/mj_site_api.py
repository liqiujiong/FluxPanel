# -*- coding:utf-8 -*-

from typing import Optional, Union
from curl_cffi import requests
from utils.request_util import retry_on_async_failure 

class MjSiteAPI:
    def __init__(
        self,
        mj_user_id: str,
        mj_site_cookie: str,
        base_url: str = 'https://www.midjourney.com/',
    ):
        self.base_url = base_url
        self.mj_user_id = mj_user_id
        self.mj_site_cookie = mj_site_cookie
        self.client = requests.AsyncSession()
        self.client.timeout = 30

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
    ) -> Union[list, dict]:
        """
        发送HTTP请求并返回JSON响应
        """
        headers = {
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'x-csrf-protection': '1',
            'Cookie': self.mj_site_cookie,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        try:
            url = self.base_url + endpoint
            if method == "GET":
                response = await self.client.get(url, params=data, headers=headers)
            elif method == "POST":
                response = await self.client.post(url, json=data, headers=headers)
            else:
                raise ValueError('method错误')

            response.raise_for_status()  # 检查请求是否成功
            response_content_type = response.headers.get("Content-Type")
            if "application/json" in response_content_type:
                return response.json()
            return response.content

        except requests.RequestsError as req_exc:
            print(f"RequestError: {req_exc}")  # 记录日志或打印错误信息
            raise

        except Exception as exc:
            print(f"Unexpected error: {exc}")  # 记录日志或打印错误信息
            raise requests.RequestException(f"Request failed: {str(exc)}") from exc

    @retry_on_async_failure()
    async def get_users_queue(self):
        path = f'api/app/users/queue?userId={self.mj_user_id}'
        data = await self._request('GET', path)
        return data

    @retry_on_async_failure()
    async def get_jobs(self, page_size=1000, cursor: str = None):
        path = f'api/pg/thomas-jobs?user_id={self.mj_user_id}&page_size={page_size}'
        if cursor:
            path += f'&cursor={cursor}'
        data = await self._request('GET', path)
        return data

    @retry_on_async_failure()
    async def get_discord_url_from_job(self, job_id):
        data = {"jobIds": [job_id]}
        path = f'api/app/get-discord-url'
        data = await self._request('POST', path, data)
        return data

    @retry_on_async_failure()
    async def cancel_job(self, job_id):
        data = {"job_id": job_id}
        path = f'api/app/jobs/cancel'
        data = await self._request('POST', path, data)
        return data

    @retry_on_async_failure()
    async def get_users_account(self):
        path = f'api/app/users/account'
        data = await self._request('GET', path)
        return data