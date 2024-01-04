import pytest

from langchain_core.runnables import RunnableLambda
from fleetchain import FletChain

@pytest.fixture
def empty_chain():

    return RunnableLambda(lambda x:x['inputs'])

def test_imports(empty_chain):

    chat = FletChain(chain = empty_chain)

    assert chat.memory == None

@pytest.mark.parametrize("name,expected", [('Boris Tvaroska', 'BT'), (None, 'U'), ('Boris Boris Tvaroska', 'BT')])
def test_initials(empty_chain, name, expected):

    if name:
        chat = FletChain(empty_chain, user_name=name)
    else:
        chat = FletChain(empty_chain)
    assert chat.user_initials == expected

