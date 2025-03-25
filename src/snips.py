#!/usr/bin/env python3

"""Snips workload manager class."""

import logging
from typing import Dict

from ops import Container
from ops.pebble import ChangeError, Layer

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)

CONTAINER_NAME = "snips"
LAYER_NAME = CONTAINER_NAME
SERVICE_NAME = CONTAINER_NAME
HTTP_PORT = 8080
SSH_PORT = 2222


class Snips:
    """Snips workload container facade."""

    def __init__(self, container: Container, hmac_key: str):
        self._container = container
        self._hmac_key = hmac_key

    @property
    def pebble_layer(self) -> Layer:
        """Pebble layer for the snips service."""
        return Layer(
            {
                "summary": "snips layer",
                "description": "pebble config layer for snips",
                "services": {
                    "snips": {
                        "override": "replace",
                        "summary": "snips",
                        "command": "/usr/bin/snips.sh",
                        "startup": "enabled",
                        "environment": self._env_vars,
                    }
                },
            }
        )

    @property
    def _env_vars(self) -> Dict:
        env_vars = {
            "SNIPS_DEBUG": True,
            "SNIPS_HMACKEY": self._hmac_key,
        }

        return env_vars

    def update_layer(self) -> bool:
        """Update service layer.

        Returns:
          True if anything changed; False otherwise
        """
        overlay = self.pebble_layer
        plan = self._container.get_plan()

        if SERVICE_NAME not in plan.services or overlay.services != plan.services:
            self._container.add_layer(LAYER_NAME, overlay, combine=True)
            try:
                self._container.replan()
                return True
            except ChangeError as e:
                logger.error(
                    "Failed to replan; pebble plan: %s; %s",
                    self._container.get_plan().to_dict(),
                    str(e),
                )
                return False

        return True
