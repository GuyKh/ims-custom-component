"""Dependency logging helpers for the IMS integration."""

from copy import copy
import logging

from loguru import logger as loguru_logger

_WEATHERIL_LOGGER_PREFIX = "weatheril"
_LOGURU_LOGGER_PREFIX = "loguru"
_LOGURU_DEFAULT_SINK_ID = 0

_loguru_sink_id: int | None = None
_active_entry_ids: set[str] = set()


class _DependencyLoggingHandler(logging.Handler):
    """Forward weatheril Loguru records into Home Assistant logging."""

    def emit(self, record: logging.LogRecord) -> None:
        if record.name.startswith(_LOGURU_LOGGER_PREFIX):
            return
        target_logger_name = f"{__package__}.{record.name}"
        target_logger = logging.getLogger(target_logger_name)
        if target_logger.isEnabledFor(record.levelno):
            forward_record = copy(record)
            forward_record.name = target_logger_name
            target_logger.handle(forward_record)


def setup_dependency_logging(entry_id: str) -> None:
    """Idempotently route Loguru logs for weatheril to standard logging."""
    global _loguru_sink_id

    _active_entry_ids.add(entry_id)

    try:
        if _loguru_sink_id is not None:
            return

        try:
            # Remove Loguru's process-wide default console sink so dependency logs
            # do not bypass Home Assistant logging.
            loguru_logger.remove(_LOGURU_DEFAULT_SINK_ID)
        except ValueError:
            pass

        _loguru_sink_id = loguru_logger.add(
            _DependencyLoggingHandler(),
            filter=lambda record: record["name"].startswith(_WEATHERIL_LOGGER_PREFIX),
            level=0,
            format="{message}",
        )
    except Exception:
        _active_entry_ids.discard(entry_id)
        if not _active_entry_ids:
            _remove_loguru_sink()
        raise


def remove_dependency_logging(entry_id: str) -> None:
    """Release dependency logging for a config entry."""
    _active_entry_ids.discard(entry_id)
    if _active_entry_ids:
        return
    _remove_loguru_sink()


def _remove_loguru_sink() -> None:
    """Tear down the Loguru sink to avoid leaking memory on integration unload."""
    global _loguru_sink_id
    if _loguru_sink_id is not None:
        try:
            loguru_logger.remove(_loguru_sink_id)
        except ValueError:
            pass
        _loguru_sink_id = None
