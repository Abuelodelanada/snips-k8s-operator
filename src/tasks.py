#!/usr/bin/env python3
# Copyright 2024 Jose C. Massón
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk


"""Tasks executed by the charm."""

import logging
from typing import List, Protocol

from ops.model import (
    BlockedStatus,
    MaintenanceStatus,
)

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)


TASK_EXECUTED = "Task '%s' executed."
TASK_FAILED = "Task '%s' failed: %s"


class Task(Protocol):
    """Task interface."""

    def execute(self) -> bool:
        """Task execution.

        Return True if the execution is successful otherwise False.
        """
        ...


class TasksFactory:
    """TaskFactory class."""

    def __init__(self, charm):
        self._charm = charm

    @property
    def tasks(self) -> List[Task]:
        """List of tasks."""
        return [
            ValidateCanConnectTask(self, self._charm._container),
            UpdatePebbleLayerTask(self, self._charm._snips),
        ]


class ValidateCanConnectTask:
    """Validate Can Connect task class."""

    def __init__(self, charm, container):
        self._class_name = __class__.__name__
        self.charm = charm
        self._container = container

    def execute(self) -> bool:
        """Task execution."""
        if not self._container.can_connect():
            msg = "Waiting for pod startup to complete"
            self.charm.unit.status = MaintenanceStatus(msg)
            logger.debug(TASK_FAILED, self._class_name, msg)
            return False

        logger.debug(TASK_EXECUTED, self._class_name)
        return True


class UpdatePebbleLayerTask:
    """Update Pebble Layer task class."""

    def __init__(self, charm, snips):
        self._class_name = __class__.__name__
        self._charm = charm
        self._snips = snips

    def execute(self) -> bool:
        """Task execution."""
        if not self._snips.update_layer():
            msg = "Unable to update Pebble layer. Check juju debug-log"
            self._charm.unit.status = BlockedStatus(msg)
            logger.debug(TASK_FAILED, self._class_name, msg)
            return False

        logger.debug(TASK_EXECUTED, self._class_name)
        return True
