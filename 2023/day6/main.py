import math


def margin(T, R):
    D = math.sqrt(T**2-4*R)
    t1 = (T-D)/2
    t2 = (T+D)/2
    beating_record_min = int(t1+1) if t1.is_integer() else math.ceil(t1)
    beating_record_max = int(t2-1) if t2.is_integer() else math.floor(t2)
    return beating_record_max - beating_record_min + 1

def main():
    pass


if __name__ == '__main__':
    # print(margin(7, 9))
    # print(margin(15, 40))
    # print(margin(30, 200))


    res = margin(55, 246) \
        * margin(82, 1441) \
        * margin(64, 1012) \
        * margin(90, 1111)
    # print(res)

    # print(margin(71530, 940200))
    print(margin(55826490, 246144110121111))

