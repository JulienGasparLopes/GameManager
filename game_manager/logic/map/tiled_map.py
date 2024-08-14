from vertyces.vertex.vertex2f import Vertex2f

from game_manager.logic.entity.tiled_entity import TileEntity
from game_manager.logic.map.map import Map
from game_manager.logic.map.tile import TILE_SIZE, VOID_TILE, Tile


class TiledMap(Map):
    _tiles: list[list[Tile]]

    def __init__(self, width: int, height: int, default_tile: Tile = VOID_TILE) -> None:
        super().__init__()
        self._tiles = [[default_tile for _ in range(width)] for _ in range(height)]

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
