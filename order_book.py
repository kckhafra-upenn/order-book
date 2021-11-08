from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
import random
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def process_order(order):
    #Your code here
    algo_total_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.creator == None).all() if order.sell_currency == "Algorand" ] )
    eth_total_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.creator == None).all() if order.sell_currency == "Ethereum" ] )
    # algo_unfilled_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.filled == None).all() if order.sell_currency == "Algorand" ] )
    # eth_unfilled_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.filled == None).all() if order.sell_currency == "Ethereum" ] )
    # print( f"Algo in = {algo_total_in:.2f}" )
    # print( "BUY AMOUNT: ", order["buy_amount"])
    order_obj = Order( sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], buy_currency=order['buy_currency'], sell_currency=order['sell_currency'], buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )
    session.add(order_obj)
    session.commit()
    # for ord in session.query(Order).filter(Order.creator == None).all():
    #     print(ord.buy_amount)

    # print( f"Eth in = {eth_total_in:.2f}" )
    # print( f"Algo in = {algo_total_in:.2f}" )
    # print("ORDER: ",order)
    

#Generate random order data
# order = {}
# platforms = ["Algorand", "Ethereum"] 
# platform = "Algorand"
# sender_pk = hex(random.randint(0,2**256))[2:] #Generate random string that looks like a public key
# receiver_pk = hex(random.randint(0,2**256))[2:] #Generate random string that looks like a public key

# other_platform = platforms[1-platforms.index(platform)]
# order['sender_pk'] = sender_pk
# order['receiver_pk'] = receiver_pk
# order['buy_currency'] = other_platform
# order['sell_currency'] = platform
# order['buy_amount'] = 3
# order['sell_amount'] = random.randint(1,10)
# process_order(order)