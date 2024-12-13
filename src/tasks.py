#!/usr/bin/env python3
# Copyright 2024 Jose C. Massón
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk


"""Tasks executed by the charm."""

from typing import Protocol

from ops.model import (
    BlockedStatus,
    MaintenanceStatus,
)

from url_manager import URLManager


class Task(Protocol):
    """Task interface."""

    def execute(self) -> bool:
        """Task execution.

        Return True if the execution is successful otherwise False.
        """
        ...


class HandleIngresMessagesTask:
    """Validate Can Connect task class."""

    def __init__(self, ingress_url, logger):
        self.ingress_url = ingress_url
        self.logger = logger

    def execute(self):
        """Task execution."""
        if url := self.ingress_url:
            self.logger.debug("Ingress is ready: '%s'.", url)
        else:
            self.logger.debug("Ingress revoked.")

        return True


class ValidateCanConnectTask:
    """Validate Can Connect task class."""

    def __init__(self, charm, container):
        self.charm = charm
        self._container = container

    def execute(self) -> bool:
        """Task execution."""
        if not self._container.can_connect():
            self.charm.unit.status = MaintenanceStatus("Waiting for pod startup to complete")
            return False

        return True


class ValidateExternalURLTask:
    """Validate External URL task class."""

    def __init__(self, charm, external_url, logger):
        self.charm = charm
        self.external_url = external_url
        self.logger = logger

    def execute(self) -> bool:
        """Task execution."""
        if ext_url := self.external_url:
            if not URLManager.validate_external_url(ext_url):
                self.logger.error("Invalid external url: '%s'", ext_url)
                self.charm.unit.status = BlockedStatus(f"Invalid external url: '{ext_url}'")
                return False
        return True


class UpdatePebbleLayerTask:
    """Update Pebble Layer task class."""

    def __init__(self, snips):
        self.snips = snips

    def execute(self) -> bool:
        """Task execution."""
        return self.snips.update_layer()
