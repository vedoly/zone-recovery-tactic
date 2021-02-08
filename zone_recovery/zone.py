import numpy as numpy


class Zone:
    def __init__(self, entry_price, zone_width, distance):
        "entry_price"
        self.up = entry_price
        self.down = entry_price - zone_width
        self.above_target = entry_price + distance
        self.below_target = entry_price - zone_width - distance

    def calculateProfit(self, t, df, money):
        state = 'Sell'
        first_money = money
        buy_cost = 0
        sell_cost = 0

        buy_unit = 0
        sell_unit = 0
        alpha = 1

        temp_money = 0

        for i, row in df.iterrows():

            if row.Price > buy_cost and state == 'Buy':
                buy_cost += 50 * alpha
                alpha *= 2
                money -= buy_cost
                buy_unit += buy_cost / row.Price
                state = 'Sell'
                print('Buy', buy_cost)

            if row.Price > sell_cost and state == 'Sell':
                sell_cost += 50 * alpha
                temp_money += sell_cost

                alpha *= 2
                money -= sell_cost
                sell_unit += sell_cost / row.Price
                state = 'Buy'
                print('Sell', sell_cost)

            if row.Price > self.above_target and state == 'Sell':
                buy_cost = 0
                money += buy_unit * row.Price

                state = 'Buy'
                print('Close Buy', buy_unit * row.Price)
                buy_unit = 0
                alpha = 1

            if row.Price < self.below_target and state == 'Buy':
                sell_cost = 0
                debt = sell_unit * row.Price
                money += temp_money - debt
                sell_unit = 0
                state = 'Sell'
                print('Close Sell', temp_money - debt)
                alpha = 1

        return money - first_money

    def monitorZone(self):
        return self.up, self.down, self.above_target, self.below_target
