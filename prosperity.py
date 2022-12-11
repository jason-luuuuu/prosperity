from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

class Trader:

    def __init__(self):
        self.pearl_position = 0
        self.banana_position = 0

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            if product == 'PEARLS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                print("PEARL ASKS")
                print(order_depth.sell_orders.items())
                print("PEARL BIDS")
                print(order_depth.buy_orders.items())

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask <= 10000:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print('PEARL BUY')
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        self.pearl_position -= best_ask_volume
                        print("Pearl Position:", self.pearl_position)

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > 10000:
                        print('PEARL SELL')
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        self.pearl_position -= best_bid_volume 
                        print("Pearl Position:", self.pearl_position)

                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!

                print("BANANA ASKS")
                print(order_depth.sell_orders.items())
                print("BANANA BIDS")
                print(order_depth.buy_orders.items())

                weightings = [0.6, 0.3, 0.1]


                sum_buy_vol = 0
                buy_vol = order_depth.buy_orders
                max_buy_vol = buy_vol[max(buy_vol.keys())]
                sum_buy_vol = max_buy_vol*0.7 

                if (max(buy_vol.keys()) -1 ) in buy_vol.keys():
                        sum_buy_vol += 0.2*buy_vol[max(buy_vol.keys())-1]
                if (max(buy_vol.keys()) -2)  in buy_vol.keys():
                        sum_buy_vol += 0.1*buy_vol[max(buy_vol.keys())-2]
                
                print("Sum_buy_vol = ", sum_buy_vol)


                sum_sell_vol = 0
                sell_vol = order_depth.sell_orders
                min_sell_vol = sell_vol[min(sell_vol.keys())]
                sum_sell_vol = min_sell_vol*0.7

                if (min(sell_vol.keys()) +1 ) in sell_vol.keys():
                        sum_sell_vol += 0.2*sell_vol[min(sell_vol.keys())+1]
                if (max(sell_vol.keys()) +2)  in sell_vol.keys():
                        sum_sell_vol += 0.1*sell_vol[min(sell_vol.keys())+2]
                
                sum_sell_vol = -1*sum_sell_vol
                print("Sum_sell_vol = ", sum_sell_vol)


                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())

                acceptable_price = (best_ask+ best_bid)/2

                acceptable_price += ((sum_buy_vol - sum_sell_vol)/(sum_buy_vol + sum_sell_vol))*3 - self.banana_position/20

                print('mid point')
                print((best_ask+ best_bid)/2)

                print('acceptable price')
                print(acceptable_price)

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask < acceptable_price:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print('BANANA BUY')
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        self.banana_position -= best_ask_volume
                        print("Banana Position", self.banana_position)

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > acceptable_price:
                        print('BANANA SELL')
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        self.banana_position -= best_bid_volume
                        print("Banana Position", self.banana_position)

                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
        
            if product == 'PINA COLADA':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                print("PEARL ASKS")
                print(order_depth.sell_orders.items())
                print("PEARL BIDS")
                print(order_depth.buy_orders.items())

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask <= 10000:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print('PEARL BUY')
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        self.pearl_position -= best_ask_volume
                        print("Pearl Position:", self.pearl_position)

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > 10000:
                        print('PEARL SELL')
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        self.pearl_position -= best_bid_volume 
                        print("Pearl Position:", self.pearl_position)

                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above
            
            if product == 'COCONUTS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                print("PEARL ASKS")
                print(order_depth.sell_orders.items())
                print("PEARL BIDS")
                print(order_depth.buy_orders.items())

                # Define a fair value for the PEARLS.
                # Note that this value of 1 is just a dummy value, you should likely change it!

                # If statement checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask <= 10000:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print('PEARL BUY')
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))
                        self.pearl_position -= best_ask_volume
                        print("Pearl Position:", self.pearl_position)

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    if best_bid > 10000:
                        print('PEARL SELL')
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))
                        self.pearl_position -= best_bid_volume 
                        print("Pearl Position:", self.pearl_position)

                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above

        return result