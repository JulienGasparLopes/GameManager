from abc import ABC

from vertyces.form.rectangle import Rectangle
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.logic.entity.entity_moveable import EntityMoveable
from game_manager.logic.map.map import Map
from game_manager.logic.map.tile import TILE_SIZE, VOID_TILE, Tile


class TiledMap(Map, ABC):
    _width_in_tiles: int
    _height_in_tiles: int
    _width: int
    _height: int
    _tiles: list[list[Tile]]

    def __init__(
        self, width_in_tiles: int, height_in_tiles: int, default_tile: Tile = VOID_TILE
    ) -> None:
        super().__init__()
        self._width = width_in_tiles * TILE_SIZE
        self._height = height_in_tiles * TILE_SIZE
        self._width_in_tiles = width_in_tiles
        self._height_in_tiles = height_in_tiles
        self._tiles = [
            [default_tile for _ in range(width_in_tiles)]
            for _ in range(height_in_tiles)
        ]

    @classmethod
    def from_tiles(cls, tiles: list[list[Tile]]) -> "TiledMap":
        # TODO: Improve error handling
        if not tiles:
            raise ValueError("Cannot create a map from an empty list of tiles")

        height = len(tiles)
        width = len(tiles[0])
        tiled_map = cls(width, height)
        tiled_map._tiles = tiles
        return tiled_map

    def get_tile_at_position(self, position: Vertex2f) -> Tile:
        return self._tiles[int(position.y // TILE_SIZE)][int(position.x // TILE_SIZE)]

    def get_tile(self, x: int, y: int) -> Tile:
        return self._tiles[y][x]

    def set_tile(self, x: int, y: int, tile: Tile) -> None:
        self._tiles[y][x] = tile

    @property
    def width_in_tiles(self) -> int:
        return self._width_in_tiles

    @property
    def height_in_tiles(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def get_tiles_in_bounds(self, bounds: Rectangle) -> list[Tile]:
        tiles = []
        for y in range(
            int(bounds._p1.y // TILE_SIZE), int(bounds._p2.y // TILE_SIZE) + 1
        ):
            for x in range(
                int(bounds._p1.x // TILE_SIZE), int(bounds._p2.x // TILE_SIZE) + 1
            ):
                if 0 <= x < self._width and 0 <= y < self._height:
                    tiles.append(self.get_tile(x, y))
        return tiles

    def _calculate_entity_new_position(
        self, delta_ns: float, entity: EntityMoveable
    ) -> Vertex2f | None:
        # TODO: try to avoid code duplication with the same method in Map
        delta_position = entity.direction.multiplied(
            entity.speed * delta_ns / 10_000_000
        )
        possible_new_positions = [
            entity.bounds._p1.translated(delta_position),
            entity.bounds._p1.translated(Vertex2f(delta_position.x, 0)),
            entity.bounds._p1.translated(Vertex2f(0, delta_position.y)),
        ]
        new_position: Vertex2f | None = None
        for possible_new_position in possible_new_positions:
            new_position = possible_new_position
            new_bounds = Rectangle(possible_new_position, entity.bounds.dimensions)
            for other_entity in self._entities.values():
                if other_entity == entity:
                    continue
                if other_entity.bounds.collides(new_bounds):
                    new_position = None
                    break

            if new_position is None:
                continue

            for tile in self.get_tiles_in_bounds(new_bounds):
                if not tile.walkable:
                    new_position = None
                    break

            if new_position is not None:
                break

        return new_position
