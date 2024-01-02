from langchain_core.runnables import RunnableLambda
from fleetchain import FletChain


def test_imports():

    chain = RunnableLambda(lambda x:x['inputs'])

    chat = FletChain(chain = chain)

    assert chat.memory == None
