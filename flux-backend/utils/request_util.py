import asyncio
import functools


def retry_on_async_failure(retries: int = 5, interval: int = 2):
    """
    装饰器: 当 API 接口抛出报错时重试。

    参数:
        retries (int): 重试次数，默认为 3 次。
        interval (int): 重试间隔（秒），默认为 5 秒。
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    # 尝试执行 API 请求
                    return await func(self, *args, **kwargs)
                except Exception as exc:
                    attempt += 1
                    if attempt < retries:
                        print(f"API 请求失败, 正在重试 {attempt}/{retries} 次，错误：{str(exc)}")
                        await asyncio.sleep(interval)  # 非阻塞地等待一定时间再重试
                    else:
                        print(f"API 请求失败, 已达最大重试次数 {retries} 次，错误：{str(exc)}")
                        raise exc
        return wrapper
    return decorator