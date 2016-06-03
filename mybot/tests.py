from bot import *
from prototype import *

def test_forecast_type():
    assert type(get_forecast('Lausanne', 'CH')) == type('')

def test_sendMessage():
    assert type(sendMessage('channel', 'txt')) == dict

def test_stop():
    stop()
    from bot import RUNNING
    assert RUNNING == False

if __name__ == "__main__":
    print('\n=== Running tests ===\n')

    test_forecast_type()
    test_sendMessage()
    test_stop()

    print('\n=== All tests passed! ===')