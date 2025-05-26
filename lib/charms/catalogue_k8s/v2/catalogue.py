# Copyright 2025 Canonical Ltd.
# See LICENSE file for licensing details.

"""Charm for providing services catalogues to bundles or sets of charms."""

import logging
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from ops.model import Application, Relation

LIBID = "fa28b361293b46668bcd1f209ada6983"
LIBAPI = 2
LIBPATCH = 1

DEFAULT_RELATION_NAME = "catalogue"

logger = logging.getLogger(__name__)

@dataclass
class CatalogueItem:
    """`CatalogueItem` represents an application entry sent to a catalogue.

    The icon is an iconify mdi string; see https://icon-sets.iconify.design/mdi.
    """

    name: str
    url: str
    icon: str
    description: str = ""

class CatalogueRequirer:
    """`CatalogueRequirer` is used to send over a `CatalogueItem`."""

    @staticmethod
    def update_item(item: CatalogueItem, relations: List["Relation"] , app: "Application", is_leader: bool = False):
        """Update item on Catalogue."""
        if not is_leader:
            return

        for relation in relations:
            relation.data[app].update(asdict(item))

class CatalogueProvider:
    """`CatalogueProvider` is the side of the relation that serves the actual service catalogue."""

    @staticmethod
    def items(relations: List["Relation"]) -> List[Dict]:
        """List of apps sent over relation data."""
        return [dict(relation.data[relation.app]) for relation in relations if relation.app and relation.units]
