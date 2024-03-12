import functools


def redirect_handle(_func):

    @functools.wraps(_func)
    def wrapper(_self):
        func = _func(_self)
        if func and func.history and func.history[0].status_code > 201:
            func.failure(f'{func.history[0].status_code}'
                         f' - Redirect! Verify cookie')
            return
    return wrapper