# From Send2Trash package's plat_osx.py file. See LICENSE_Send2Trash file for license information from that package

# Copyright 2017 Virgil Dupras

# This software is licensed under the "BSD" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.hardcoded.net/licenses/bsd_license

from ctypes import cdll, byref, Structure, c_char, c_char_p
from ctypes.util import find_library

Foundation = cdll.LoadLibrary(find_library('Foundation'))
CoreServices = cdll.LoadLibrary(find_library('CoreServices'))

get_status_comment_string = Foundation.GetMacOSStatusCommentString
get_status_comment_string.restype = c_char_p
make_reference = CoreServices.FSPathMakeRefWithOptions
move_to_trash_sync = CoreServices.FSMoveObjectToTrashSync

make_reference_not_follow_symlink = 0x01
file_operation_default_options = 0


class FSRef(Structure):
    _fields_ = [('hidden', c_char * 80)]


def check_options_result(options_result):
    if options_result:
        message = get_status_comment_string(options_result).decode('utf-8')
        raise OSError(message)


def send_to_trash(path: str):
    """Sends a file or folder to the macOS Trash folder using the system's C library. Slightly modified from
    Virgil Dupras's `Send2Trash <https://pypi.org/project/Send2Trash/#description>`_ package.

    :param path: Path of file or folder to be sent to trash.
    :type path: str
    """
    if not isinstance(path, bytes):
        path = path.encode('utf-8')
    filepath = FSRef()
    options = make_reference_not_follow_symlink
    options_result = make_reference(path, options, byref(filepath), None)

    check_options_result(options_result)
    options = file_operation_default_options
    options_result = move_to_trash_sync(byref(filepath), None, options)

    check_options_result(options_result)
