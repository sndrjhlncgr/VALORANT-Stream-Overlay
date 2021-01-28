def rankNames(code=None):
    rank_names = {
        3: 'Iron I',
        4: 'Iron II',
        5: 'Iron III',
        6: 'Bronze I',
        7: 'Bronze II',
        8: 'Bronze III',
        9: 'Silver I',
        10: 'Silver II',
        11: 'Silver III',
        12: 'Gold I',
        13: 'Gold II',
        14: 'Gold III',
        15: 'Platinum I',
        16: 'Platinum II',
        17: 'Platinum III',
        18: 'Diamond I',
        19: 'Diamond II',
        20: 'Diamond III',
        21: 'Immortal I',
        22: 'Immortal II',
        23: 'Immortal III',
        24: 'Radiant',
    }

    return rank_names.get(code, "Invalid rank")
