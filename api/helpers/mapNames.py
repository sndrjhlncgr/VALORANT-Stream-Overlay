def mapNames(map=None):
    maps = {
        '/Game/Maps/Duality/Duality': 'Bind',
        '/Game/Maps/Bonsai/Bonsai': 'Split',
        '/Game/Maps/Ascent/Ascent': 'Ascent',
        '/Game/Maps/Port/Port': 'Icebox',
        '/Game/Maps/Triad/Triad': 'Haven',
        '': 'Unknown'
    }

    return maps.get(map, "Invalid map")

