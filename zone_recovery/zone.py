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

    def calculateProfit(self, t, df, modulation):

        open = []
        hold = []

        first_price = df.iloc[0].Price
        open.append(first_price)

        for i, row in df[1:].iterrows():
            if row.Price > 0:
                pass

        return t, df.iloc[0].Price, modulation
