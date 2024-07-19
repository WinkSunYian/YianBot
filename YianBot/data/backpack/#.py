import os
import json

"RelationalArray"


class BackpackControl:
    """
    用户背包工具
    """

    backpack_path = "data\\backpack\\{}.json"

    relational: dict = {}
    data: list = []

    def __init__(self, user_id):
        self.user_backpack = self.backpack_path.format(user_id)
        if not os.path.exists(self.user_backpack):
            with open(self.user_backpack, 'w', encoding='utf-8-sig') as fp:
                json.dump([], fp)
        self.read_backpack()
        self.read_relational()

    def save(self):
        with open(self.user_backpack, "w", encoding='utf-8-sig') as fp:
            json.dump(self.data, fp, ensure_ascii=False)

    def read_backpack(self):
        with open(self.user_backpack, encoding='utf-8-sig') as fp:
            self.data = json.load(fp)

    def read_relational(self):
        with open(self.backpack_path.format(0), encoding='utf-8-sig') as fp:
            self.relational = json.load(fp)

    def get_id(self, key):
        for item in self.relational:
            if key == self.relational[item]:
                return item
        return key

    def __getitem__(self, key):
        key = self.get_id(key)

        for item in self.data:
            if key == item["id"]:
                return item['value']
        return 0

    def __setitem__(self, key, value):
        key = self.get_id(key)

        for i in range(len(self.data)):
            if key == self.data[i]['id']:
                self.data[i]['value'] = value
                break
        else:
            self.data.append(
                {
                    "id": self.get_id(key),
                    "value": value
                }
            )
            # 根据ID排序
            self.data = sorted(self.data, key=lambda x: x["id"])

    def __repr__(self):
        return str(self.data)

    def __iter__(self):
        return iter(self.data)


if __name__ == "__main__":
    user_id = "7345222"
    template = BackpackControl(user_id)
    template["方糖"] = 1
    print(template)
