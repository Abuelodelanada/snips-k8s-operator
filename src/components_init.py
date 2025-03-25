#!/usr/bin/env python3
# Copyright 2023 Jose C. Massón
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Components Initialiser class."""

from secret_manager import SecretManager
from snips import Snips


class ComponentsInitialiser:
    """Initialise the components for the charm."""

    def __init__(self, charm, container_name):
        self.charm = charm
        self.container_name = container_name

    def initialise_components(self):
        """Initialise the components for the charm."""
        container = self.charm.unit.get_container(self.container_name)
        secret_manager = SecretManager(self.charm)
        snips = Snips(container, secret_manager.hmac_key)
        return container, snips
