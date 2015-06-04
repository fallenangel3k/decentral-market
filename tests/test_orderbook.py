from tsukiji import orderbook as ob


def test_create_msg_incrementing_message_id():
    first_message = ob.create_msg()
    second_message = ob.create_msg()

    assert first_message['message-id'] == 0, 'Expected 0, got {}'.format(first_message['message-id'])
    assert second_message['message-id'] == 1, 'Expected 1, got {}'.format(second_message['message-id'])


def test_create_msg():
    message = ob.create_msg()
    assert type(message) == dict


def test_create_msg_passing_options():
    options = {
        'hello': 'world',
    }

    message = ob.create_msg(options=options)
    assert 'hello' in message
    assert message['hello'] == 'world'


def test_create_msg_passing_options_overriding_default():
    options = {
        'id': 1234,
    }

    message = ob.create_msg(options=options)
    assert 'id' in message
    assert message['id'] == 1234


def test_create_ask():
    import datetime
    ask = ob.create_ask(1, 1, datetime.datetime.now())
    assert ask['type'] == 'ask'
    assert ask['price'] == 1
    assert ask['quantity'] == 1
    assert len(ob.offers) == 1
