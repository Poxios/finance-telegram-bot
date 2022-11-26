def generate_text_bar_graph(length: int, min_value: int, score: int, max_value: int):
    if score <= min_value:
        return f'[{min_value} ⚡{"―"*(length-1)} {max_value}]'
    elif max_value <= score:
        return f'[{min_value} {"―"*(length-1)}⚡ {max_value}]'

    def roundUp(num: int): return int(num) + \
        1 if (num - int(num)) >= 0.5 else int(num)

    percent = (score-min_value) / (max_value-min_value)
    bar_count_front = roundUp((length)*percent)-1
    bar_count_back = length - bar_count_front-1
    graph_text = ('―'*bar_count_front) + '⚡' + ('―'*bar_count_back)
    return f'[{min_value} {graph_text} {max_value}]'
