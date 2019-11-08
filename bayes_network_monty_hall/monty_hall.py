from bayesian.bbn import build_bbn

# 定义选择有奖品的门的概率为 1/3
def door_with_prize(prize_door):
    return 1 / 3

# 定义猜测选中门号的概率，也为 1/3
def door_choosed(guest_door):
    return 1 / 3

def door_monty(prize_door, guest_door, monty_door):
    if prize_door == guest_door:  # 选中了有车的门
        if prize_door == monty_door:
            return 0     # 没有获得奖项
        else:
            return 1 / 2   # 选择下一个有山羊的门，现在只有两个选择
    elif prize_door == monty_door:
        return 0         # 仍然没有选中含有奖项的门
    elif guest_door == monty_door:
        return 0         
    else:
        # 其他情况
        return 1

if __name__ == '__main__':
    get_result = build_bbn(
                    door_with_prize,
                    door_choosed,
                    door_monty,
                    domains=dict(
                    # 定义每种选项的可选择情况
                        prize_door=['1', '2', '3'],
                        guest_door=['1', '2', '3'],
                        monty_door=['1', '2', '3']))


get_result.q()
get_result.q(guest_door='1')
get_result.q(guest_door='1', monty_door='2')
get_result.q(guest_door='3', monty_door='2')
get_result.q(guest_door='1', monty_door='3')
get_result.q(guest_door='2', monty_door='1')

