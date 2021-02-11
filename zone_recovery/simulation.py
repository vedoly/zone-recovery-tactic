from zone import Zone


def makeDecision(prev_price, current_price, zone: Zone, state: str):

    if (prev_price > zone.up and current_price < zone.up or current_price == zone.up) and state == 'w8 4 Buy':
        return 'Open Buy', 'w8 4 Sell'

    if (prev_price < zone.down and current_price > zone.down or current_price == zone.down) and state == 'w8 4 Sell':
        return 'Open Sell', 'w8 4 Buy'

    if (prev_price < zone.above_target and current_price > zone.above_target or current_price == zone.above_target) and state == 'w8 4 Sell':
        return 'Close Buy', 'w8 4 Buy'

    if (prev_price > zone.below_target and current_price < zone.below_target or current_price == zone.below_target) and state == 'w8 4 Buy':
        return 'Close Sell', 'w8 4 Buy'

    return 'Steady', state


def simulation(df, entry_amount, limit=99, expected_profit=4, multiplier=2, money=100, zone_width=1, distance=4):

    buy_unit, sell_unit, buy_hold, sell_hold = 0, 0, 0, 0
    alpha = 1

    log = []
    for i, current in df.iterrows():

        if buy_hold == 0 and sell_hold == 0:
            zone = Zone(current.Price, current.Price *
                        zone_width / 100, current.Price * distance / 100)
            state, action = 'w8 4 Sell', 'Open Buy'

        else:
            action, state = makeDecision(
                prev_price, current.Price, zone, state)

        if entry_amount * alpha > money:
            action = 'Cut Loss'

        if action == 'Open Buy':
            buy_hold += entry_amount*alpha
            money -= entry_amount*alpha
            buy_unit += entry_amount*alpha / current.Price
            alpha *= multiplier

        if action == 'Open Sell':
            sell_hold += entry_amount*alpha
            money -= entry_amount*alpha
            sell_unit += entry_amount*alpha / current.Price
            alpha *= multiplier

        if action == 'Cut Loss' or action == 'Close Buy' or action == 'Close Sell':
            money += buy_unit * current.Price + 2*sell_hold - sell_unit * current.Price
            buy_unit = 0
            sell_unit = 0
            buy_hold, sell_hold = 0, 0
            alpha = 1
            state = 'w8 4 Sell'

        if(action != 'Steady'):
            print(action, current.Price, money, buy_hold, sell_hold)

        log.append((action, money, buy_hold, sell_hold))
        prev_price = current.Price
    return log


def simulation0(df, limit=0, expected_profit=4, alpha=1, money=10, zone_width=1, distance=4):

    money = limit

    temp_money, buy_cost, sell_cost = 0, 0, 0

    buy_unit, sell_unit, buy_hold, sell_hold = 0, 0, 0, 0

    profit = 0

    for i, row in df.iterrows():

        current_price = row.Price

        if buy_hold == 0 and sell_hold == 0:
            zone = Zone(current_price, current_price *
                        zone_width / 100, current_price * distance / 100)
            state, action = 'w8 4 Sell', 'Open Buy'

        else:
            action, state = makeDecision(
                prev_price, current_price, zone, state)

        if buy_hold + sell_hold > limit:
            action, state = 'Cut Loss', 'w8 4 Sell'

        if action == 'Cut Loss' or action == 'Close Buy' or action == 'Close Sell':

            buy_cost = 0
            money += buy_unit * row.Price
            buy_unit = 0

            sell_cost = 0
            debt = sell_unit * row.Price
            money += 2*temp_money - debt
            sell_unit = 0
            buy_hold, sell_hold = 0, 0
            alpha = 1
            temp_money = 0

        if action == 'Open Buy':
            if buy_hold + sell_hold + alpha > limit:
                action = 'Cut Loss'
                pass
            buy_cost += 1 * alpha
            buy_hold += alpha
            alpha *= 2
            money -= buy_cost
            buy_unit += buy_cost / row.Price

            # state = 'Sell'
            # print('Open Buy', buy_cost, row.Price,money)

        if action == 'Open Sell':
            if buy_hold + sell_hold + alpha > limit:
                action = 'Cut Loss'
                pass

            sell_cost += 1 * alpha
            sell_hold += alpha
            temp_money += sell_cost
            alpha *= 2
            money -= sell_cost
            sell_unit += sell_cost / row.Price

        if action == 'Cut Loss' or action == 'Close Buy' or action == 'Close Sell':

            buy_cost = 0
            money += buy_unit * row.Price
            buy_unit = 0

            sell_cost = 0
            debt = sell_unit * row.Price
            money += 2*temp_money - debt
            sell_unit = 0
            buy_hold, sell_hold = 0, 0
            alpha = 1
            temp_money = 0

            # state = 'Buy'
            # print('Open Sell', sell_cost,money)

        # if sell_unit == 0 and buy_unit == 0:
        #     zone = Zone(current_price,current_price* zone_width / 100, current_price* distance / 100)

        if(action != 'Steady'):
            print(action, current_price, money, buy_hold, sell_hold)

        prev_price = current_price
    return money
