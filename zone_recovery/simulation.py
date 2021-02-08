from zone import Zone


def makeDecision(prev_price, current_price, zone: Zone, state: str):

    if (prev_price > zone.up and current_price < zone.up or current_price == zone.up) and state == 'w8 4 Buy':
        return 'Open Buy', 'w8 4 Sell'

    if (prev_price < zone.down and current_price > zone.down or current_price == zone.down) and state == 'w8 4 Sell':
        return 'Open Sell', 'w8 4 Buy'

    if (prev_price < zone.above_target and current_price > zone.above_target or current_price == zone.above_target) and state == 'w8 4 Sell':
        return 'Close Buy', 'w8 4 Buy'

    if (prev_price > zone.below_target and current_price < zone.below_target or current_price == zone.below_target) and state == 'w8 4 Buy':
        return 'Close Sell', 'w8 4 Sell'

    return 'Steady', state


def simulation(df, limit=4, alpha=2, money=1000):

    state = 'w8 4 Sell'
    action = 'Open Buy'
    first_money = money
    temp_money = 0
    buy_cost = 1
    sell_cost = 0

    sell_unit = 0

    first_price = df.iloc[0].Price
    prev_price = first_price
    buy_unit = buy_cost / first_price

    money -= buy_cost
    print(action, first_price, money, 1, 0)

    zone = Zone(first_price, first_price * 0.01, first_price * 0.04)

    buy_hold = 1
    sell_hold = 0

    for i, row in df[1:].iterrows():

        current_price = row.Price
        action, state = makeDecision(prev_price, current_price, zone, state)

        if alpha > 8:

            buy_cost = 0
            money += buy_unit * row.Price
            buy_unit = 0

            sell_cost = 0
            debt = sell_unit * row.Price
            money += temp_money - debt
            sell_unit = 0
            buy_hold, sell_hold = 0, 0
            alpha = 1
            action = 'Cut Loss'

        if action == 'Open Buy':
            buy_cost += 1 * alpha
            buy_hold += alpha
            alpha *= 2
            money -= buy_cost
            buy_unit += buy_cost / row.Price

            # state = 'Sell'
            # print('Open Buy', buy_cost, row.Price,money)

        if action == 'Open Sell':
            sell_cost += 1 * alpha
            sell_hold += alpha
            temp_money += sell_cost
            alpha *= 2
            money -= sell_cost
            sell_unit += sell_cost / row.Price

            # state = 'Buy'
            # print('Open Sell', sell_cost,money)

        if action == 'Close Buy':

            buy_cost = 0
            money += buy_unit * row.Price

            # state = 'Buy'
            # print('Close Buy', buy_unit * row.Price,money)
            buy_hold = 0
            buy_unit = 0
            alpha = 1

        if action == 'Close Sell':

            sell_cost = 0
            debt = sell_unit * row.Price
            # print(temp_money,debt)
            money += 2*temp_money - debt
            sell_unit = 0
            sell_hold = 0
            # state = 'Sell'
            # print('Close Sell', temp_money - debt,money)
            alpha = 1

        if sell_unit == 0 and buy_unit == 0:
            zone = Zone(current_price, current_price *
                        0.01, current_price * 0.04)

        if(action != 'Steady'):
            print(action, current_price, money, buy_hold, sell_hold)

        prev_price = current_price
    print(money-first_money)
