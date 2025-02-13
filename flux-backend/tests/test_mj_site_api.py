import datetime
import json
import pytest
from module_admin.entity.do.mj_account_do import MjAccount
from utils.mj_site_api import MjSiteAPI

pytest_plugins = ('pytest_asyncio', )

mj_site_api = MjSiteAPI(
    mj_user_id='3a86ecfe-928b-4d4a-b439-658b10c069a5',
    mj_site_cookie='AMP_MKTG_437c42b22c=JTdCJTdE; _ga=GA1.1.670949375.1739030405; _gcl_au=1.1.14849391.1739030405; __Host-Midjourney.AuthUserTokenV3_r=AMf-vBzqfDqvdH79eSl4wGEh2hFaLg--AdC1VUf5ncPp-YrLKhaohfBTS8T6valrOBODZpfXzrgQtByvdyO0VlKoT6RoXMb02zB8NChDTeYinIZy3k7yk1vmGvy6CBEXyJ_9GK_qdeAcgHnrJEzYGZsGVoir3iPDhXXD0oWovDvnATjpDenn8mV5s3zTJ4kIqbea5KHe_d4i1Ufi4tCpm3_2j06xVWzT1D3nm0sSm4L6vz0GDQDqMn4GdVluUTcFgTHXjpYN0rU4OzAbvw0K_H2ZJk4u2eAo6SZSAELv9UYYA2OnyeibjLmmD30aeDAu97IALB5xSBKL; __Host-Midjourney.AuthUserTokenV3_i=eyJhbGciOiJSUzI1NiIsImtpZCI6ImE0MzRmMzFkN2Y3NWRiN2QyZjQ0YjgxZDg1MjMwZWQxN2ZlNTk3MzciLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoicWRkMTIzIiwicGljdHVyZSI6ImZhZjI1OWFlMTQ5MDk0NjRjMTM1Yjk1NTVlY2UwYTkwIiwibWlkam91cm5leV9pZCI6IjNhODZlY2ZlLTkyOGItNGQ0YS1iNDM5LTY1OGIxMGMwNjlhNSIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9hdXRoam91cm5leSIsImF1ZCI6ImF1dGhqb3VybmV5IiwiYXV0aF90aW1lIjoxNzM5MDMwNDE2LCJ1c2VyX2lkIjoiWFBHZDROOExTQmE0alBjWUpyOW5jOHBaSDhuMSIsInN1YiI6IlhQR2Q0TjhMU0JhNGpQY1lKcjluYzhwWkg4bjEiLCJpYXQiOjE3MzkwMzgwOTksImV4cCI6MTczOTA0MTY5OSwiZW1haWwiOiJwb29uZ2lhcmRpbmFjOEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJkaXNjb3JkLmNvbSI6WyIxMTEzMjE2NjU3NDIzMzM5NjYxIl0sImVtYWlsIjpbInBvb25naWFyZGluYWM4QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6ImRpc2NvcmQuY29tIn19.MIEUeZLiULhxh8K60ltNTv5C0qjZXy2fb--PzT1tQ_y77zv6DV89OUDX-gZBETv_uhHrGrkmFVBfqFk4kGYWoPWl3qZ0j_uaoLflCk_LOiUK14QMA7Zfu7j3vMD6QB1IV2KHTsBW6F8n8rTmQLUNiaY0z9izl39a-Ko6P25Y0bceHhwO0L7QWp97E93T-_3MI7sey1g03081UQkA6H_nQTN3VTYB8BXel7iA7KDcLkxifbHOtlAYiH1cWHPQla-VxCQTFMGLkAEqE-ZjoQzsVQ-wJgou2t7p0qIDiJjlkL29dotdfjPdZsSuD_Ys1vbYCYWlZTCAuZR0QOkz1qcKWw; __cf_bm=q8ztnGMZttAXcjxX9fcDMj8c8tRZY7OiHZmLBzY5kU4-1739041184-1.0.1.1-1n5zF4ZQeveq64vlJ1UA5uDUg0XhdYby.lgrBmQNuf2IXi_w9rqnNzb8WsZ8yatEQrrdboxpSPNlytdF162DMg; cf_clearance=zU58ryzAVA3d7TSqGmgVCHNYwHxWXoTxuj_soFr9zoQ-1739041388-1.2.1.1-S8v9v0FQrebpd5QTa8ALCVPnbSZ0KAxYwmK3iFsv56At5jFiwT1hqbbPcLMA.jZjNvFTHMFHysfr1SGf7wXXSGEPPBL1D7e4wJO.INU2dU5SMM6LBZSEOQ.2zFI5qqKW9sBia41rUGAUANnHvIKhf1G4Cp3gO0Ya9fL7Vud4y7Ww.pN7jVx7e3JE4Li.Nr84u29vVD76.uXWbzOau_K0YWmVDmw88Egu0E5MDvjwWj6lVSNvHVwf4PS1jdr.o0ovRq12M0cUbg7paV53c__5BxMPnRV3kpnZd7ZuvU50Nv0; AMP_437c42b22c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJjNjczNWIwNy1mN2Y5LTRlYTgtYjZmMC1kYzRiNWZkZTA2M2IlMjIlMkMlMjJ1c2VySWQlMjIlM0ElMjIzYTg2ZWNmZS05MjhiLTRkNGEtYjQzOS02NThiMTBjMDY5YTUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM5MDMwNDA0MjQyJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczOTA0MTYyOTQwOCUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzk5JTdE; _ga_Q0DQ5L7K0D=GS1.1.1739039040.2.1.1739041630.0.0.0'
)
@pytest.mark.asyncio
class TestMjSiteAPI:
    async def test_get_users_queue(self):
        data = await mj_site_api.get_users_queue()
        print(data)

    async def test_get_discord_url_from_job(self):
        data = await mj_site_api.get_discord_url_from_job('efc57380-2daf-4cf8-87e9-7f798e30e24e')
        print(data) 
    
    async def test_cancel_job(self):
        data = await mj_site_api.cancel_job('1d1c6e20-7e7c-4ebb-a492-d1e75beb1891')
        print(data)

    async def test_get_jobs(self):
        data = await mj_site_api.get_jobs()
        print(data)

    async def test_get_users_account(self):
        data = await mj_site_api.get_users_account()
        print(json.dumps(data, indent=4))
        # user_id = data['user']['mjId']
        # subscription_type = data['userData']['plan']['type']
        mj_account = MjAccount()
        mj_account.mj_id = data['user']['mjId']
        mj_account.plan = data['userData']['plan']['type']
        mj_account.status = data['userData']['status']
        mj_account.expire_time = datetime.datetime.strptime(data['userData']['billing_period']['end'], '%Y-%m-%d')
        mj_account.subscribe_time = data['userData']['billing_period']['start']
        mj_account.total_jobs = data['user']['abilities']['total_jobs']
        mj_account.user_id = data['user']['mjId']
        mj_account.last_monitor_time = datetime.now()
        print(mj_account)
