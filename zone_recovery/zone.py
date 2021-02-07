import numpy as numpy


class Zone:
    def __init__(self, up, down, above_target, below_target):
        self.up = up
        self.down = down
        self.above_target = above_target
        self.below_target = below_target
        self.zone_width = up-down
        self.up_distance = above_target-up
        self.down_distance = below_target-down

    def calculateProfit(self, t, df, money):
        state = 'Sell'
        first_money = money
        buy_cost = 0
        sell_cost = 0

        buy_unit = 0
        sell_unit = 0

        for i, row in df.iterrows():

            if row.Price > buy_cost and state == 'Buy':
                buy_cost += 50
                money -= buy_cost
                buy_unit += buy_cost / row.Price
                state = 'Sell'

            if row.Price > sell_cost and state == 'Sell':
                sell_cost += 50
                money -= sell_cost
                sell_unit += sell_cost / row.Price
                state = 'Buy'

            if row.Price > self.above_target and state == 'Sell':
                buy_cost = 0
                money += buy_unit * row.Price
                buy_unit = 0
                state = 'Buy'

            if row.Price > self.above_target and state == 'Buy':
                sell_cost = 0
                money += sell_unit * row.Price
                sell_unit = 0
                state = 'Sell'

        return money - first_money
