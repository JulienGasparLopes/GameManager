"""Tile class for the map."""

TILE_SIZE = 40
"""Tile size. May be modified."""


class Tile:
    _walkable: bool = True

    def __init__(self, walkable: bool = True) -> None:
        self._walkable = walkable

    @property
    def walkable(self) -> bool:
        return self._walkable


VOID_TILE = Tile(walkable=False)
