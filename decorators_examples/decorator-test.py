import asyncio
import logging

logger = logging.getLogger()


def catch_pipeline_errors_methods_async_args(func):
    async def catch_errors_methods(self, *args, **kwargs):
        try:
            print(f"ZviDebug-> args={args}")
            print(f"ZviDebug-> kwargs={kwargs}")
            return await func(self, **kwargs, *args)

        except Exception as exc:
            logger.exception(f"Intercepted a pipeline exception in function %s --> \n %s", func.__name__, exc)
            raise

    return catch_errors_methods


def catch_pipeline_errors_methods_async_kwargs(func):
    async def catch_errors_methods(*args, **kwargs):
        try:
            logger.debug(f"ZviDebug-> args={args}")
            logger.debug(f"ZviDebug-> kwargs={kwargs}")
            return await func(*args, **kwargs)

        except Exception as exc:
            logger.exception(f"Intercepted a pipeline exception in function %s --> \n %s", func.__name__, exc)
            raise

    return catch_errors_methods


class TestDecorators:

    def __init__(self, num: str):
        self.num = num

    @catch_pipeline_errors_methods_async_args
    async def my_method(self, my_list: list[str], list_two: list[str], list_three: list[str]) -> dict[str, list]:
        print(my_list)
        print(list_two)
        print(list_three)
        return {"the_list": my_list, "the_list2": list_two, "the_list3": list_three }


async def main():
    test_dec = TestDecorators("5")
    print(await test_dec.my_method(my_list=[1, 2, 3, 4], clist_two=[4, 3, 2, 1], list_three=[5, 6, 7, 8]))


asyncio.run(main())
