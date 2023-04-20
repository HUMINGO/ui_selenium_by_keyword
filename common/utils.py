# coding = utf-8

def get_list(list1: list):
    """
    剔除掉一个列表中的none元素
    :param list1:
    :return:
    """
    target_list = []
    for i in list1:
        if i is not None:
            target_list.append(i)

    return target_list


a = [1, 3, None, None]

print(get_list(a))
