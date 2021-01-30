def rankNames(code=None):
    rank_names = {
        3: ['Iron 1', '#696969'],
        4: ['Iron 2', '#696969'],
        5: ['Iron 3', '#696969'],
        6: ['Bronze 1', '#a86832'],
        7: ['Bronze 2', '#a86832'],
        8: ['Bronze 3', '#a86832'],
        9: ['Silver 1', '#bdb9b9'],
        10: ['Silver 2', '#bdb9b9'],
        11: ['Silver 3', '#bdb9b9'],
        12: ['Gold 1', '#f7c62f'],
        13: ['Gold 3', '#f7c62f'],
        14: ['Gold 3', '#f7c62f'],
        15: ['Platinum 1', '#2fd6f7'],
        16: ['Platinum 2', '#2fd6f7'],
        17: ['Platinum 3', '#2fd6f7'],
        18: ['Diamond 1', '#af4dff'],
        19: ['Diamond 2', '#af4dff'],
        20: ['Diamond 3', '#af4dff'],
        21: ['Immortal 1', '#f02673'],
        22: ['Immortal 2', '#f02673'],
        23: ['Immortal 3', '#f02673'],
        24: ['Radiant', '#f0ad26'],
    }

    return rank_names.get(code, "Invalid rank")
