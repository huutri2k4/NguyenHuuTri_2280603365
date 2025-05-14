def truy_cap_phan_tu(tuple_data):
    first_element = tuple_data[0]
    last_element = tuple_data[-1]
    return first_element, last_element
input_tuple = eval(input("nhap tuple, vi du (1,2,3): "))
first, last = truy_cap_phan_tu(input_tuple)
print("phan tu dau tien:", first)
print("phan tu cuoi cung:", last)