#
# li = [1, 3, 55, 111, 989, 1010, 1111, 3232]
#
#
# def binary_seach(li, val):
#     low = 0
#     high = len(li) - 1
#     while low <= high:
#         mid = (low + high) // 2
#         if li[mid] == val:
#             return True
#         elif li[mid] < val:
#             low = mid + 1
#         else:
#             high = mid - 1
#     else:
#         return False
#
#
# print(binary_seach(li, 111))


# def bubble_sort(li):
#     n = len(li) - 1
#     for i in range(n):
#         flag = False
#         for j in range(i + 1, n):
#             if li[j] < li[i]:
#                 li[j], li[i] = li[i], li[j]
#                 flag = True
#         if flag == False:
#             break
#
#
# li = [2, 5, 4, 8, 9, 0, 1, 6, 7, 3, 11, 33]
#
# bubble_sort(li)
# print(li)

# li = [2, 5, 4, 8, 9, 0, 1, 6, 7, 3, 11, 33]
#
#
# def select_sort(li):
#     for i in range(len(li)):
#         min_index = i
#         for j in range(i + 1, len(li)):
#             if li[min_index] < li[j]:
#                 min_index = j
#             li[min_index], li[i] = li[i], li[min_index]
#
# select_sort(li)
# print(li)

#
# def insert_sort(li):
#     for i in range(len(li)):
#         j = i
#         while j > 0:
#             if li[j] < li[j - 1]:
#                 li[j], li[j - 1] = li[j - 1], li[j]
#                 j -= 1
#             else:
#                 break
#
#
# li = [2, 5, 4, 8, 9, 313131, 1, 6, 7, 3, 11, 33, 1, 33, 231, 4444]
# insert_sort(li)
# print(li)


# def select_sort(li):
#     for i in range(len(li)):
#         min_index = i
#         for j in range(i + 1, len(li)):
#             if li[min_index] > li[j]:
#                 min_index = j
#         li[min_index], li[i] = li[i], li[min_index]
# li = [2, 5, 4, 8, 9, 313131, 1, 6, 7, 3, 11, 33, 1, 33, 231, 4444]
# select_sort(li)
# print(li)

li = [2, 5, 4, 8, 9, 313131, 1, 6, 7, 3, 11, 33, 1, 33, 231, 4444]


# def bubble_sort(li):
#     n = len(li) - 1
#     for i in range(n):
#         flag = False
#         for j in range(i + 1, n):
#             if li[i] > li[j]:
#                 li[i], li[j] = li[j], li[i]
#                 flag = True
#         if flag == False:
#             break
# bubble_sort(li)
# print(li)


# def sort(li, low, mid, high):
#     i = low
#     j = mid + 1
#     li_tmp = []
#     while i <= mid and j <= high:
#         if li[i] < li[j]:
#             li_tmp.append(li[i])
#             i += 1
#         else:
#             li_tmp.append(li[j])
#             j += 1
#     while i <= mid:
#         li_tmp.append(li[i])
#         i += 1
#     while j <= high:
#         li_tmp.append(li[j])
#         j += 1
#     for i in range(low, high + 1):
#         li[i] = li_tmp[i - low]
#
#
# def merge_sort(li, low, high):
#     mid = (low + high) // 2
#     if low < high:
#         merge_sort(li, low, mid)
#         merge_sort(li, mid + 1, high)
#         sort(li, low, mid, high)
#
#
# merge_sort(li, 0, len(li) - 1)
# print(li)

# def sort(li, low, mid, high):
#     i = low
#     j = mid + 1
#     li_tmp = []
#     while i <= mid and j <= high:
#         if li[i] < li[j]:
#             li_tmp.append(li[i])
#             i += 1
#         else:
#             li_tmp.append(li[j])
#             j += 1
#     while i <= mid:
#         li_tmp.append(li[i])
#         i += 1
#     while j <= high:
#         li_tmp.append(li[j])
#         j += 1
#     for i in range(low, high + 1):
#         li[i] = li_tmp[i - low]
#
#
# def merge_sort(li, low, high):
#     if low < high:
#         mid = (low + high) // 2
#         merge_sort(li, low, mid)
#         merge_sort(li, mid + 1, high)
#         sort(li, low, mid, high)
#
#
# merge_sort(li, 0, len(li) - 1)
# print(li)

# def sort(li, low, mid, high):
#     i = low
#     j = mid + 1
#     li_tmp = []
#     while i <= mid and j <= high:
#         if li[i] < li[j]:
#             li_tmp.append(li[i])
#             i += 1
#         else:
#             li_tmp.append(li[j])
#             j += 1
#     while i <= mid:
#         li_tmp.append(li[i])
#         i += 1
#     while j <= high:
#         li_tmp.append(li[j])
#         j += 1
#     for i in range(low, high + 1):
#         li[i] = li_tmp[i - low]
#
#
# def merge_sort(li, low, high):
#     if low < high:
#         mid = (low + high) // 2
#         merge_sort(li, low, mid)
#         merge_sort(li, mid + 1, high)
#         sort(li, low, mid, high)
#
#
# merge_sort(li, 0, len(li) - 1)
# print(li)


# def partition(li, left, right):
#     mid_value = li[left]
#     while left < right:
#         while left < right and mid_value <= li[right]:
#             right -= 1
#         li[left] = li[right]
#         while left < right and mid_value >= li[left]:
#             left += 1
#         li[right] = li[left]
#     li[left] = mid_value
#     return left
#
#


# def quick_sort(li, left, right):
#     if left < right:
#         mid = partition(li, left, right)
#         quick_sort(li, left, mid)
#         quick_sort(li, mid + 1, right)
# quick_sort(li,0,len(li) - 1)
# print(li)
def sift(li, low, high):
    tmp = li[low]
    i = low
    j = 2 * i + 1
    while j <= high:
        if j < high and li[j + 1] > li[j]:
            j += 1
        if tmp < li[j]:
            li[i] = li[j]
            i = j
            j = 2 * i + 1
        else:
            break
    li[i] = tmp


def heap_sort(li):
    n = len(li)
    for i in range(n // 2 - 1, -1, -1):
        sift(li, i, n - 1)
    for i in range(n - 1, -1, -1):
        li[0], li[i] = li[i], li[0]
        sift(li, 0, i - 1)


heap_sort(li)
print(li)
