from pony.orm import Database, Required, db_session, select, commit, desc
from utils.module import db, User, Backpack, Item, DialogueHistory
from datetime import datetime, timedelta


def get_user(user_id):
    with db_session:
        user = User.get(user=str(user_id))
        if user is None:
            user = User(user=str(user_id))
            commit()
        return user


class UserBackpackManager:
    def __init__(self, user_id: int):
        self.user_id = str(user_id)
        if not isinstance(user_id, int):
            raise TypeError("参数必须是整数")
        if 5 > len(self.user_id) or len(self.user_id) > 10:
            raise TypeError("参数长度错误")

    @db_session
    def get_user(self):
        user = User.get(user=self.user_id)
        if not user:
            user = User(user=self.user_id)
            # 当创建用户时，同时为其创建一个backpack
            user.backpack = Backpack(user=user)
            commit()
        elif not user.backpack:
            # 如果用户存在但没有backpack，为其创建一个
            user.backpack = Backpack(user=user)
            commit()
        return user

    @db_session
    def _get_item(self, item_name):
        user = self.get_user()
        item = Item.get(name=item_name, backpack=user.backpack)
        return item

    @db_session
    def __getitem__(self, item_name):
        item = self._get_item(item_name)
        return item.quantity if item else 0

    @db_session
    def __setitem__(self, item_name, quantity):
        user = self.get_user()
        item = self._get_item(item_name)
        if item:
            item.quantity = quantity
        else:
            item = Item(name=item_name, quantity=quantity, backpack=user.backpack)
        commit()

    @db_session
    def __iter__(self):
        user = self.get_user()
        # 在会话内部预先加载所有项
        items = list(user.backpack.item)  # 强制立即加载所有项
        return iter(items)


class DialogueHistoryManager:
    def __init__(self, db):
        self.db = db

    @db_session
    def add_dialogue(self, user_id, my_msg, assistant_msg):
        """
        添加新的对话记录，遵循两个规则：
        1. 如果与上次对话时间超过10分钟，则清空之前的所有记录。
        2. 用户最多只能拥有5条对话记录。

        :param user_id: 用户的ID。
        :param my_msg: 用户的消息。
        :param assistant_msg: 助手的回复。
        """
        user = self.db.User.get(user=str(user_id))
        if not user:
            return

            # 获取用户的最新一条对话记录
        last_dialogue = select(d for d in self.db.DialogueHistory if d.user == user).order_by(
            desc(self.db.DialogueHistory.timestamp)).first()

        # 检查是否超过10分钟
        if last_dialogue and datetime.now() - last_dialogue.timestamp > timedelta(minutes=10):
            # 清空所有现有对话记录
            select(d for d in self.db.DialogueHistory if d.user == user).delete()

            # 如果没有超过10分钟，检查是否达到5条记录的限制
        elif select(d for d in self.db.DialogueHistory if d.user == user).count() >= 5:
            # 删除最早的记录（时间升序排序后的第一条）
            oldest_dialogue = select(d for d in self.db.DialogueHistory if d.user == user).order_by(
                self.db.DialogueHistory.timestamp).first()
            oldest_dialogue.delete()

            # 添加新的对话记录
        self.db.DialogueHistory(user=user, my_msg=my_msg, assistant_msg=assistant_msg, timestamp=datetime.now())

    @db_session
    def get_dialogues_for_user(self, user_id):
        """
        获取指定用户的所有对话记录。

        :param user_id: 用户的ID。
        :return: 指定用户的对话记录列表。
        """
        user = self.db.User.get(user=str(user_id))
        if not user:
            return []

            # 获取用户的最新一条对话记录
        last_dialogue = select(d for d in self.db.DialogueHistory if d.user == user).order_by(
            desc(self.db.DialogueHistory.timestamp)).first()

        # 检查是否超过10分钟
        if last_dialogue and datetime.now() - last_dialogue.timestamp > timedelta(minutes=10):
            # 清空所有现有对话记录
            select(d for d in self.db.DialogueHistory if d.user == user).delete()
            return []

        dialogues = select(d for d in self.db.DialogueHistory if d.user == user).order_by(
            self.db.DialogueHistory.timestamp)
        return list(dialogues)
