# Copyright 2021 Canonical Ltd.
# See LICENSE file for licensing details.

"""Charm for providing services catalogues to bundles or sets of charms."""

import logging

from ops.model import Application, Relation
from typing import Dict, List

LIBID = "fa28b361293b46668bcd1f209ada6983"
LIBAPI = 2
LIBPATCH = 1

DEFAULT_RELATION_NAME = "catalogue"

logger = logging.getLogger(__name__)


class CatalogueItem:
    """`CatalogueItem` represents an application entry sent to a catalogue.

    The icon is an iconify mdi string; see https://icon-sets.iconify.design/mdi.
    """

    def __init__(self, name: str, url: str, icon: str, description: str = ""):
        self.name = name
        self.url = url
        self.icon = icon
        self.description = description


class CatalogueConsumer:
    """`CatalogueConsumer` is used to send over a `CatalogueItem`."""

    @staticmethod
    def update_item(item: CatalogueItem, relations: List[Relation] , app: Application, is_leader: bool = False):
        if not is_leader:
            return

        for relation in relations:
            relation.data[app]["name"] = item.name
            relation.data[app]["description"] = item.description
            relation.data[app]["url"] = item.url
            relation.data[app]["icon"] = item.icon


class CatalogueProvider():
    """`CatalogueProvider` is the side of the relation that serves the actual service catalogue."""

    @staticmethod
    def items(relations: List[Relation]) -> List[Dict]:
        """A list of apps sent over relation data."""
        return [
            {
                "name": relation.data[relation.app].get("name", ""),
                "url": relation.data[relation.app].get("url", ""),
                "icon": relation.data[relation.app].get("icon", ""),
                "description": relation.data[relation.app].get("description", ""),
            }
            for relation in relations
            if relation.app and relation.units
        ]
