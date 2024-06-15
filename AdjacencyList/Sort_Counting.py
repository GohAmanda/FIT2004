# Function counting sort
def sort_counting(new_list):

    '''
    Precondition: new_list have at least 1 item
    '''

    # find the maximum
    max_item = new_list[0]
    for item in new_list:
        if item > max_item:
            max_item = item
    #print(max_item)

    # initialize count array
    count_array = [0] * (max_item+1)
    #print(count_array)

    # Update count array
    for item in new_list:
        count_array[item] = count_array[item] + 1
    #print(count_array)

    index = 0
    # update input array
    for i in range(len(count_array)):
        item = i
        frequency = count_array[i]
        for i in range(frequency):
            new_list[index] = item
            index = index + 1

    # new_list will be sorted
    return new_list

# Function counting sort alpha
def sort_counting_alpha(new_list): 

    '''
    Precondition: new_list have at least 1 item
    '''

    # find the maximum
    max_item = ord(new_list[0])-97
    for item in new_list:
        item = ord(item)-97
        if item > max_item:
            max_item = item
    print(max_item)

    # initialize count array
    count_array = [0] * (max_item+1) #there's a problem here
    #print(count_array)

    # Update count array
    for item in new_list:
        count_array[item] = count_array[item] + 1
    #print(count_array)

    index = 0
    # update input array
    for i in range(len(count_array)):
        item = i
        frequency = count_array[i]
        for i in range(frequency):
            new_list[index] = item
            index = index + 1

    # new_list will be sorted
    return new_list


def sort_counting_stable(new_list):

    '''
    Precondition: new_list have at least 1 item
    '''

    # find the maximum
    max_item = new_list[0]
    for item in new_list:
        if item > max_item:
            max_item = item
    #print(max_item)

    # initialize count array
    count_array = [[]] * (max_item+1)
    #print(count_array)

    # Update count array
    for item in new_list:
        count_array[item].append(item)
    #print(count_array)
    return
    #print(count_array)

    index = 0
    # update input array
    for i in range(len(count_array)):
        item = i
        frequency = count_array[i]
        for i in range(frequency):
            new_list[index] = item
            index = index + 1

    # new_list will be sorted
    return new_list



list_a = [6,3,1,7,2,8,1,7]
#list_a = ["a", "e", "b", "c", "d", "e", "a"]
print(list_a)
list_a = sort_counting_stable(list_a)
print(list_a)



# check
# for i in range(0, len(list_a)-1):
#     if list_a[i] <= list_a[i+1]:
#         continue
#     else:
#         print("Fail!")
# print("Pass!")

