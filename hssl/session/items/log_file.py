import os
from logging import StreamHandler
from typing import Optional, Type, Union

from ...logging import DEBUG, LOGGER, Formatter, log
from .. import SessionItem, Unset, register_session_item

_LOG_HANDLER = None
_FILE_STREAM = None


def _setter(path: Optional[Union[str, Type[Unset]]]):
    # pylint: disable=global-statement
    global _FILE_STREAM, _LOG_HANDLER
    if _LOG_HANDLER is not None:
        LOGGER.removeHandler(_LOG_HANDLER)
        _LOG_HANDLER = None
    if _FILE_STREAM is not None:
        _FILE_STREAM.close()
        _FILE_STREAM = None
    if isinstance(path, str):
        log(DEBUG, "opening log file stream: %s", path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        _FILE_STREAM = open(path, "a")
        _LOG_HANDLER = StreamHandler(_FILE_STREAM)
        _LOG_HANDLER.setFormatter(Formatter(fancy_formatting=False))
        LOGGER.addHandler(_LOG_HANDLER)


register_session_item("log_file", SessionItem(setter=_setter, default=None))
