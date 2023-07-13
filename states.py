from aiogram.dispatcher.filters.state import State, StatesGroup


class Ourstates(StatesGroup):
    text_task = State()
    notes_task = State()
    bool_task = State()
    main_state = State()
    del_state = State()
    remid_state = State()
    remid_state_1 = State()
