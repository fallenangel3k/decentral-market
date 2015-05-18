import datetime

own_bids = []
own_asks = []
bids = []
asks = []
message_id = 0


def create_ask(id, price, quantity, timeout):
    return create_msg(id, type='ask', price=price, quantity=quantity, timeout=timeout)


def create_bid(id, price, quantity, timeout):
    return create_msg(id, type='bid', price=price, quantity=quantity, timeout=timeout)


def create_trade(id, quantity, trade_id):
    return create_msg(id, type='trade', quantity=quantity, trade_id=trade_id)


def create_greeting(id):
    return create_msg(id, type='greeting')


def create_msg(id, type=None, price=None, quantity=None, timeout=None, trade_id=None):
    '''
    Standard for message passing.

    Message can have 5 types: ask, bid, trade, cancel, greeting.
    Depending on the type of message, an argument might be mandatory.
    '''
    global message_id

    message = {
        "id": id,
        "message-id": message_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "type": type,
    }

    message_id = message_id + 1

    if type in ["ask", "bid"]:
        message.update({
            "price": price,
            "quantity": quantity,
            "timeout": timeout
        })
        if type == "ask":
            own_asks.append(message)
        else:
            own_bids.append(message)
    elif type == "trade":
        message.update({
            "quantity": quantity,
            "trade-id": trade_id,
        })
    elif type == "cancel":
        message.update({
            "trade-id": trade_id,
        })

    return message


def trade_offer(their_offer, own_offer):
    return create_trade(
        id = own_offer['id'],
        quantity = own_offer['quantity'],
        trade_id = "{};{}".format(their_offer['id'], their_offer['message-id'])
    )

def match_bid(bid, asks=asks):
    '''Match a bid of your own with the lowest ask from the other party.'''
    matching_asks = filter(lambda ask: ask['price'] <= bid['price'], asks)
    return lowest_offer(matching_asks)


def match_incoming_bid(bid):
    '''Match a bid from the other party with your own asks.'''
    matching_asks = filter(lambda ask: ask['price'] >= bid['price'], asks)
    return highest_offer(matching_asks)

def match_ask(ask, bids=bids):
    '''Match an ask of your own with the highest bid from the other party.'''
    matching_bids = filter(lambda bid: bid['price'] >= ask['price'], bids)
    return highest_offer(matching_bids)


def match_incoming_ask(ask):
    '''Match an ask from the other party with your own bids'''
    matching_bids = filter(lambda bid: bid['price'] <= ask['price'], own_bids)
    return lowest_offer(matching_bids)

def lowest_offer(offers):
    return min(offers, key=lambda x: x['price']) if offers else None


def highest_offer(offers):
    return max(offers, key=lambda x: x['price']) if offers else None


def remove_offer(id, message_id, offers=[]):
    for offer in offers:
        if offers['id'] == id and offers['message-id'] == message_id:
            offers.remove(offer)
