# 这个文件"导入"上面的模块
from day4_module_demo import shuffle_cards, pick_one

cards = ["The Fool", "The Magician", "The Star"]

print("洗牌结果：", shuffle_cards(cards))
print("抽一张：", pick_one(cards))