from zone_recovery.zone import Zone


def makeDecisionLegacy(prev_price, current_price, zone: Zone, state: str):

    if (prev_price > zone.up and current_price < zone.up or current_price == zone.up) and state == 'w8 4 Buy':
        return 'Open Buy', 'w8 4 Sell'

    if (prev_price < zone.down and current_price > zone.down or current_price == zone.down) and state == 'w8 4 Sell':
        return 'Open Sell', 'w8 4 Buy'

    if (prev_price < zone.above_target and current_price > zone.above_target or current_price == zone.above_target) and state == 'w8 4 Sell':
        return 'Close Buy', 'w8 4 Buy'

    if (prev_price > zone.below_target and current_price < zone.below_target or current_price == zone.below_target) and state == 'w8 4 Buy':
        return 'Close Sell', 'w8 4 Buy'

    return 'Steady', state


def makeDecision(prev_price, current_price, zone: Zone, state: str):

    if (prev_price < zone.below_target and current_price > zone.below_target or current_price == zone.below_target) and state == 'w8 4 Buy':
        return 'Close Sell', 'w8 4 Buy'

    if (prev_price > zone.above_target and current_price < zone.above_target or current_price == zone.above_target) and state == 'w8 4 Sell':
        return 'Close Buy', 'w8 4 Buy'

    if (prev_price > zone.up and current_price < zone.up or current_price == zone.up) and state == 'w8 4 Buy':
        return 'Open Buy', 'w8 4 Sell'

    if (prev_price < zone.down and current_price > zone.down or current_price == zone.down) and state == 'w8 4 Sell':
        return 'Open Sell', 'w8 4 Buy'

    return 'Steady', state


def changeValue(holds, units, current_Price, state, leverage):
    out = holds.copy()
    for i in range(len(holds)):
        out[i] += (units[i]*current_Price-holds[i]) * state * leverage
    return out


def caculateNextTradeAmount(expected_profit, entry_amount, buy_hold, sell_hold, zone_width=1, distance=4):

    expected_profit = (expected_profit) / 100
    current_option_hold, opposit_option_hold = min(
        buy_hold, sell_hold), max(buy_hold, sell_hold)

    if buy_hold + sell_hold == 0:
        return entry_amount

    return ((opposit_option_hold) * (zone_width/100 + distance/100) + expected_profit) / (distance/100) - current_option_hold


def simulation(df, entry_amount, open_limit=99, expected_profit=4, multiplier=2, money=100, zone_width=1, distance=4, leverage=1, guarantee_limit=0.3):

    buy_unit, sell_unit, buy_hold, sell_hold = list(), list(), list(), list()
    buy_current, sell_current = list(), list()
    alpha = entry_amount
    first_money = money
    count = 0
    mininum_balance = money
    log = []
    print('Simulating ...')
    for i, current in df.iterrows():
        # if i % 10000 == 0:
        #     print('.', end='')
        if(money + sum(buy_current+[0]) + sum(sell_current+[0])) < guarantee_limit * first_money:
            print(action, current.Price, money, buy_current, sell_current,
                  money + sum(buy_current+[0]) + sum(sell_current+[0]))

            print("Broken")
            return log
        if len(buy_hold) == 0 and len(sell_hold) == 0:
            zone = Zone(current.Price, current.Price *
                        zone_width / 100, current.Price * distance / 100)
            state, action = 'w8 4 Sell', 'Open Buy'
            alpha = entry_amount
        else:
            action, state = makeDecision(
                prev_price, current.Price, zone, state)

            if action != 'Steady':
                alpha = caculateNextTradeAmount(expected_profit, entry_amount, sum(
                    buy_hold), sum(sell_hold), zone_width, distance)

        if alpha > money:
            action = 'Cut Loss'

        if action[:4] == 'Open' and count >= open_limit:
            action = 'Cut Loss'

        if action == 'Open Buy':
            buy_hold.append(alpha)
            money -= alpha
            buy_unit.append(alpha / current.Price)
            count += 1
            # buy_price.append(current.Price)

        if action == 'Open Sell':
            sell_hold.append(alpha)
            money -= alpha
            sell_unit.append(alpha / current.Price)
            count += 1
            # sell_price.append(current.Price)

        buy_current = changeValue(
            buy_hold, buy_unit, current.Price, 1, leverage)
        sell_current = changeValue(
            sell_hold, sell_unit, current.Price, -1, leverage)

        if action == 'Cut Loss' or action == 'Close Buy' or action == 'Close Sell':
            money += sum(buy_current+[0]) + sum(sell_current+[0])
            buy_unit = []
            sell_unit = []
            buy_hold, sell_hold = [], []
            buy_current, sell_current = list(), list()
            alpha = entry_amount
            state = 'w8 4 Sell'
            count = 0
        mininum_balance = min(mininum_balance, money +
                              sum(buy_current+[0]) + sum(sell_current+[0]))
        if(action != 'Steady'):
            print(action, current.Price, money, buy_current, sell_current,
                  money + sum(buy_current+[0]) + sum(sell_current+[0]))

        log.append((action, current.Price, money, buy_current, sell_current,
                    money + sum(buy_current+[0]) + sum(sell_current+[0]), current.Month, current.Day))
        prev_price = current.Price
    print(money, mininum_balance)
    return log
