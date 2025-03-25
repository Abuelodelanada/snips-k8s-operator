# Copyright 2023 jose
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest.mock import PropertyMock, patch

import ops
import ops.testing

from charm import SnipsK8SOperatorCharm


class TestCharm(unittest.TestCase):
    def setUp(self):
        mock_hmac_key = patch(
            "secret_manager.SecretManager.hmac_key", new_callable=PropertyMock, return_value="D10S"
        )
        self.mock_hmac_key = mock_hmac_key.start()
        self.harness = ops.testing.Harness(SnipsK8SOperatorCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_snips_pebble_ready(self):
        # Expected plan after Pebble ready with default config
        expected_plan = {
            "services": {
                "snips": {
                    "override": "replace",
                    "summary": "snips",
                    "command": "/usr/bin/snips.sh",
                    "startup": "enabled",
                    "environment": {
                        "SNIPS_DEBUG": True,
                        "SNIPS_HMACKEY": "D10S",
                    },
                }
            }
        }
        # Simulate the container coming up and emission of pebble-ready event
        self.harness.container_pebble_ready("snips")
        # Get the plan now we've run PebbleReady

        # import pdb
        # pdb.set_trace()
        updated_plan = self.harness.get_container_pebble_plan("snips").to_dict()
        # Check we've got the plan we expected
        self.assertEqual(expected_plan, updated_plan)
        # Check the service was started
        service = self.harness.model.unit.get_container("snips").get_service("snips")
        self.assertTrue(service.is_running())
        # Ensure we set an ActiveStatus with no message
        self.assertEqual(self.harness.model.unit.status, ops.ActiveStatus())
