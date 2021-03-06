import shippai

from . import exceptions
from ._native import ffi, lib


errors = shippai.Shippai(ffi, lib)


def string_rv(c_str):
    try:
        return ffi.string(c_str).decode('utf-8')
    finally:
        lib.vdirsyncer_free_str(c_str)


def item_rv(c):
    return ffi.gc(c, lib.vdirsyncer_free_item)


def get_error_pointer():
    return ffi.new("ShippaiError **")


def check_error(e):
    try:
        errors.check_exception(e[0])
    except errors.ItemNotFound as e:
        raise exceptions.NotFoundError(e)
    except errors.ItemAlreadyExisting as e:
        raise exceptions.AlreadyExistingError(e)
    except errors.WrongEtag as e:
        raise exceptions.WrongEtagError(e)
