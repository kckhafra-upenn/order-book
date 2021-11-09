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
    order_obj = Order( sender_pk=newOrder['sender_pk'],receiver_pk=newOrder['receiver_pk'], buy_currency=newOrder['buy_currency'], sell_currency=newOrder['sell_currency'], buy_amount=newOrder['buy_amount'], sell_amount=newOrder['sell_amount'] )
    session.add(order_obj)
    session.commit()
    lastInserted=session.query(Order).all()[len(session.query(Order).all())-1]
    # print(lastInserted.id)
    
    queryResults = session.query(Order).all()
    for existingOrder in queryResults:
        # print("ID: ",existingOrder.id)
        # if (existingOrder.filled==None and existingOrder.sender_pk==newOrder["sender_pk"] and existingOrder.receiver_pk==newOrder["receiver_pk"] and existingOrder.buy_currency==newOrder["buy_currency"] and existingOrder.sell_currency==newOrder["sell_currency"] and (existingOrder.sell_amount/existingOrder.buy_amount)>=(newOrder["buy_amount"]/newOrder["sell_amount"])):
        if (existingOrder.filled==None and existingOrder.buy_currency==newOrder["sell_currency"] and existingOrder.sell_currency==newOrder["buy_currency"] and (existingOrder.sell_amount/existingOrder.buy_amount)>=(newOrder["buy_amount"]/newOrder["sell_amount"])):
            existingOrder.filled=datetime.now()
            lastInserted.filled=datetime.now()
            lastInserted.counterparty_id=existingOrder.id
            existingOrder.counterparty_id=lastInserted.id
            # print(existingOrder.filled, existingOrder.counterparty_id, )
            if(existingOrder.sell_amount<lastInserted.buy_amount):
                nOrder = {}
                nOrder["created_by"]=lastInserted.id
                nOrder['sender_pk'] = lastInserted.sender_pk
                nOrder['receiver_pk'] = lastInserted.receiver_pk
                nOrder['buy_currency'] = lastInserted.buy_currency
                nOrder['sell_currency'] = lastInserted.sell_currency
                nOrder['sell_amount'] = lastInserted.sell_amount
                nOrder['buy_amount'] = (lastInserted.sell_amount-existingOrder.sell_amount)
                lastInserted.child=existingOrder.id
                process_order(nOrder)
            if(lastInserted.sell_amount<existingOrder.buy_amount):
                nOrder = {}
                nOrder["created_by"]=existingOrder.id
                nOrder['sender_pk'] = existingOrder.sender_pk
                nOrder['receiver_pk'] = existingOrder.receiver_pk
                nOrder['buy_currency'] = existingOrder.buy_currency
                nOrder['sell_currency'] = existingOrder.sell_currency
                nOrder['sell_amount'] = existingOrder.sell_amount
                nOrder['buy_amount'] = (existingOrder.sell_amount-lastInserted.sell_amount)
                existingOrder.child=lastInserted.id
                process_order(nOrder)
            break

    

#Generate random order data
# order = {}
# platforms = ["Algorand", "Ethereum"] 
# platform = "Algorand"
# sender_pk = hex(random.randint(0,2**256))[2:] #Generate random string that looks like a public key
# receiver_pk = hex(random.randint(0,2**256))[2:] #Generate random string that looks like a public key

# other_platform = platforms[1-platforms.index(platform)]
# # order['sender_pk'] = sender_pk
# # order['receiver_pk'] = receiver_pk
# # order['buy_currency'] = other_platform
# # order['sell_currency'] = platform
# # order['buy_amount'] = random.randint(1,10)
# # order['sell_amount'] = random.randint(1,10)
# order['sender_pk'] = 'f5e0f3b0595ee86720c3dbe0e9a73b986fe049acea41a9aa2045d9f8898ebd8b'
# order['receiver_pk'] = '8635437bcdb06d02ffa7285610aa6c7267d433a8e7162749a0f4f38823230960'
# order['buy_currency'] = 'Ethereum'
# order['sell_currency'] = 'Algorand'
# order['buy_amount'] = 2
# order['sell_amount'] = 7

# process_order(order)