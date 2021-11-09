from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Order
import random
engine = create_engine('sqlite:///orders.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def process_order(newOrder):
    # print(newOrder)
    #Your code here
    # algo_total_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.creator == None).all() if order.sell_currency == "Algorand" ] )
    # eth_total_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.creator == None).all() if order.sell_currency == "Ethereum" ] )
    # algo_unfilled_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.filled == None).all() if order.sell_currency == "Algorand" ] )
    # eth_unfilled_in = sum( [order.sell_amount for order in session.query(Order).filter(Order.filled == None).all() if order.sell_currency == "Ethereum" ] )
    # print( f"Algo in = {algo_total_in:.2f}" )
    # print( "BUY AMOUNT: ", order["buy_amount"])
    # print("NEWORDER: ",newOrder)
    newOrder["filled"]=None
    newOrder["counterparty_id"]=None
    queryResults = session.query(Order).all()
    # newOrder["id"]=
    # print("HEY: ",queryResults)
    for existingOrder in queryResults:
        # print("ID: ",existingOrder.id)
        if (existingOrder.filled==None and existingOrder.sender_pk==newOrder["sender_pk"] and existingOrder.receiver_pk==newOrder["receiver_pk"] and existingOrder.buy_currency==newOrder["buy_currency"] and existingOrder.sell_currency==newOrder["sell_currency"] and (existingOrder.sell_amount>=newOrder["buy_amount"] or existingOrder.buy_amount>=newOrder["sell_amount"])):
            existingOrder.filled==datetime.now()
            newOrder["filled"]=datetime.now()
            newOrder["counterparty_id"]=existingOrder.id
            # existingOrder.counterparty_id=newOrder["id"]
            # print("BITCH")
    order_obj = Order( sender_pk=newOrder['sender_pk'],receiver_pk=newOrder['receiver_pk'], buy_currency=newOrder['buy_currency'], sell_currency=newOrder['sell_currency'], buy_amount=newOrder['buy_amount'], sell_amount=newOrder['sell_amount'] )
    session.add(order_obj)
    session.commit()
    # lastInserted=session.query(Order).all()[len(session.query(Order).all())-1]
    # lastInserted.counterparty_id=
    # for existingOrder in session.query(Order).all():
    #     print("IDSS: ",existingOrder.id)
    # print("END: ",end)

        

        
        #     existingOrder.filled = datetime
    # order_obj = Order( sender_pk=order['sender_pk'],receiver_pk=order['receiver_pk'], buy_currency=order['buy_currency'], sell_currency=order['sell_currency'], buy_amount=order['buy_amount'], sell_amount=order['sell_amount'] )
    # session.add(order_obj)
    # session.commit()
    # print("time",datetime.now())
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
# order['buy_amount'] = random.randint(1,10)
# order['sell_amount'] = random.randint(1,10)

# process_order(order)