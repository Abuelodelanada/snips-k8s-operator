#!/usr/bin/env python3
# Copyright 2024 Jose C. Massón
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Secret Manager class."""

import secrets
import string

from ops.model import SecretNotFoundError


class SecretManager:
    """Secret Manager class."""

    def __init__(self, charm):
        self.charm = charm

    @property
    def hmac_key(self) -> str:
        """Retrieve or create hmac-key."""
        try:
            secret = self.charm.model.get_secret(label="hmac-key")
        except SecretNotFoundError:
            secret = self.charm.app.add_secret(
                {"hmac-key": self._generate_hmac_key()}, label="hmac-key"
            )
        return secret.get_content()["hmac-key"]

    def _generate_hmac_key(self) -> str:
        """Generate a random 24 character symmetric key used to sign URLs."""
        chars = string.ascii_letters + string.digits
        return "".join(secrets.choice(chars) for _ in range(24))
