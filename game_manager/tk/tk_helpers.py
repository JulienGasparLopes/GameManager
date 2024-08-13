from vertyces.vertex.vertex3f import Vertex3f


def v3f_to_hex(color: Vertex3f) -> str:
    return "#{:02x}{:02x}{:02x}".format(int(color.x), int(color.y), int(color.z))
