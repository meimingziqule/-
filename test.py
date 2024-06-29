from collections import Counter

def find_most_two_num(input_list):
    """
    Find the two most common elements in a list.
    
    Parameters:
    input_list (list): The list of elements to be analyzed.
    
    Returns:
    tuple: A tuple containing the two most common elements, or (None, None) if less than two elements exist.
    """
    # 检查输入是否为列表类型
    if not isinstance(input_list, list):
        raise ValueError("Input must be a list.")
    
    # 使用Counter来计算元素的频率，并直接获取最频繁的两个元素
    counter = Counter(input_list)
    most_common = counter.most_common(2)
    
    # 如果列表为空或只有一个元素，most_common将少于两个元素，此时返回(None, None)
    if len(most_common) < 2:
        return None, None
    else:
        # 返回出现次数最多的两个元素
        return most_common[0][0], most_common[1][0]
    
a,b = find_most_two_num([1,1,2,2,3,3,3])
print(a,b)