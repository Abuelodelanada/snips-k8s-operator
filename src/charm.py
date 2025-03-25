#!/usr/bin/env python3
# Copyright 2023 Jose C. Massón
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

https://discourse.charmhub.io/t/4208
"""

import logging
from typing import List

from ops import main
from ops.charm import CharmBase
from ops.model import ActiveStatus

from components_init import ComponentsInitialiser
from snips import CONTAINER_NAME
from tasks import Task, TasksFactory

# Log messages can be retrieved using juju debug-log
logger = logging.getLogger(__name__)


class SnipsK8SOperatorCharm(CharmBase):
    """Snips charm class."""

    def __init__(self, framework):
        super().__init__(framework)
        initialiser = ComponentsInitialiser(self, CONTAINER_NAME)
        self._container, self._snips = initialiser.initialise_components()
        self._tasks: List[Task] = TasksFactory(self).tasks
        self._observe_events()

    def _observe_events(self):
        self.framework.observe(self.on.snips_pebble_ready, self._reconcile)
        self.framework.observe(self.on.update_status, self._reconcile)
        self.framework.observe(self.on.config_changed, self._reconcile)

    def _reconcile(self, _) -> None:
        """Event processing hook that is common to all events to ensure idempotency."""
        for task in self._tasks:
            if not task.execute():
                return

        self.unit.status = ActiveStatus()


if __name__ == "__main__":
    main(SnipsK8SOperatorCharm)
