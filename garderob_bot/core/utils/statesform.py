from aiogram.fsm.state import StatesGroup, State

class StepsMailing(StatesGroup):
    INSERT_TEXT = State()
    INSERT_MEDIA = State()
    NOT_ACTIVE = State()
    SENDING = State()
class StatesCustomer(StatesGroup):
    NONE = State()
    ASKING_QUESTION = State()
    OFFERING = State()
    WAITING = State()
    CHATTING = State()
class StatesOpDB(StatesGroup):
    INSERT_INFO = State()
    GET_INFO = State()
    ADD_ORDER = State()
    GET_ORDER = State()
    GET_ORDERS = State()
    SET_ORDER_STATE = State()
    NONE = State()
class StatesOperator(StatesGroup):
    ONLINE = State()
    OFFLINE = State()
class forward(StatesGroup):
    FORWARD_MESSAGE = State()