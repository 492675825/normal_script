'''
需求：通过冒泡排序的方式将 [5,4,6,2,3,1] 排成正序
'''


class bubble_sort:
    def __init__(self):
        self.raw_list = [5, 4, 6, 2, 3, 1]

    def sort(self):
        for j in range(len(self.raw_list)):
            for i in range(len(self.raw_list)):
                if i < len(self.raw_list) - 1:
                    first_number = self.raw_list[i]
                    second_number = self.raw_list[i + 1]
                    if first_number > second_number:
                        temp = first_number
                        first_number = second_number


                        second_number = temp
                        self.raw_list[i] = first_number
                        self.raw_list[i + 1] = second_number
                        print(self.raw_list)
        return self.raw_list


if __name__ == '__main__':
    data = bubble_sort()
    result_list = data.sort()
    print(result_list)
