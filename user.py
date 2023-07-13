class User:
    main_dict: list
    alarm: str | None
    user_id: int
    del_num: int
    alarm_state: bool

    def __init__(self, user_id: int, main_dict: list, alarm: str = None, del_nume: int=None, alarm_state: bool=False):
        self.user_id = user_id
        self.main_dict = [[], [], []]
        self.alarm = alarm
        self.del_num=del_nume
        self.alarm_state=alarm_state
