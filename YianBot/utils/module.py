from pony.orm import Database, Required, PrimaryKey, Optional, Set
from datetime import datetime

db = Database()


class User(db.Entity):
    _table_ = "user"
    id = PrimaryKey(int, auto=True)
    user = Required(str, max_len=10, unique=True)
    backpack = Optional("Backpack", reverse="user")
    dialogues = Set("DialogueHistory")  # 用户参与的对话历史


class Backpack(db.Entity):
    # 背包表
    _table_ = "backpack"
    id = PrimaryKey(int, auto=True)
    user = Optional("User", nullable=True, default=None, reverse="backpack")
    item = Set("Item", reverse="backpack")


class Item(db.Entity):
    # 道具表
    _table_ = "item"
    id = PrimaryKey(int, auto=True)
    backpack = Optional("Backpack", default=None, nullable=True, reverse="item")
    name = Required(str)
    quantity = Required(int, default=0)
    can_gift = Required(bool, default=True)
    data = Optional(str, default="")


class DialogueHistory(db.Entity):
    _table_ = "dialogue_history"
    id = PrimaryKey(int, auto=True)
    user = Required("User")
    my_msg = Optional(str, default="")
    assistant_msg = Optional(str, default="")
    timestamp = Required(datetime, default=datetime.now)


db.bind('mysql', user='SunYian', password='bLrMhdkHfbtzmXhw', host='db.sunyian.cloud', database='yianbot')
db.generate_mapping(create_tables=True)

#
# db.drop_table("User", if_exists=True, with_all_data=True)
# db.drop_table("Backpack", if_exists=True, with_all_data=True)
# db.drop_table("Item", if_exists=True, with_all_data=True)
# db.drop_table("DialogueHistory", if_exists=True, with_all_data=True)
