def rankNames(code=None):
    rank_names = {
        3: ['Iron 1', 'linear-gradient(315deg, #2d3436 0%, #d3d3d3 74%)', '#696969'],
        4: ['Iron 2', 'linear-gradient(315deg, #2d3436 0%, #d3d3d3 74%)', '#696969'],
        5: ['Iron 3', 'linear-gradient(315deg, #2d3436 0%, #d3d3d3 74%)', '#696969'],
        6: ['Bronze 1', 'linear-gradient(315deg, #772f1a 0%, #f2a65a 74%)', '#a86832'],
        7: ['Bronze 2', 'linear-gradient(315deg, #772f1a 0%, #f2a65a 74%)', '#a86832'],
        8: ['Bronze 3', 'linear-gradient(315deg, #772f1a 0%, #f2a65a 74%)', '#a86832'],
        9: ['Silver 1', 'linear-gradient(315deg, #2d3436 0%, #d3d3d3 74%)', '#bdb9b9'],
        10: ['Silver 2', 'linear-gradient(315deg, #2d3436 0%, #d3d3d3 74%)', '#bdb9b9'],
        11: ['Silver 3', 'linear-gradient(315deg, #2d3436 0%, #d3d3d3 74%)', '#bdb9b9'],
        12: ['Gold 1', 'linear-gradient(315deg, #f06543 0%, #ffbe3d 74%)', '#f7c62f'],
        13: ['Gold 3', 'linear-gradient(315deg, #f06543 0%, #ffbe3d 74%)', '#f7c62f'],
        14: ['Gold 3', 'linear-gradient(315deg, #f06543 0%, #ffbe3d 74%)', '#f7c62f'],
        15: ['Platinum 1', 'linear-gradient(315deg, #007ea7 0%, #80ced7 74%)', '#2fd6f7'],
        16: ['Platinum 2', 'linear-gradient(315deg, #007ea7 0%, #80ced7 74%)', '#2fd6f7'],
        17: ['Platinum 3', 'linear-gradient(315deg, #007ea7 0%, #80ced7 74%)', '#2fd6f7'],
        18: ['Diamond 1', 'linear-gradient(315deg, #f8ceec 0%, #a88beb 74%)', '#af4dff'],
        19: ['Diamond 2', 'linear-gradient(315deg, #f8ceec 0%, #a88beb 74%)', '#af4dff'],
        20: ['Diamond 3', 'linear-gradient(315deg, #f8ceec 0%, #a88beb 74%)', '#af4dff'],
        21: ['Immortal 1', 'linear-gradient(326deg, #861657 0%, #ffa69e 74%)', '#f02673'],
        22: ['Immortal 2', 'linear-gradient(326deg, #861657 0%, #ffa69e 74%)', '#f02673'],
        23: ['Immortal 3', 'linear-gradient(326deg, #861657 0%, #ffa69e 74%)', '#f02673'],
        24: ['Radiant', 'linear-gradient(315deg, #e8c99b 0%, #e8bc85 74%)', '#f0ad26'],
    }

    return rank_names.get(code, "Invalid rank")
