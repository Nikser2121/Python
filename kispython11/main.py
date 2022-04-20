import struct


def main(data):
    return struct_a_parse(data, 4)


def unpack_char(data, offset):
    data = struct.unpack('<3s', data[offset:offset + 3])
    data = data[0]
    data = data.decode('utf-8')
    return data, offset + 3


def unpack_uint(data, offset, bytes_num):
    if bytes_num == 1:
        data = struct.unpack('<B', data[offset:offset + bytes_num])
    elif bytes_num == 2:
        data = struct.unpack('<H', data[offset:offset + bytes_num])
    elif bytes_num == 4:
        data = struct.unpack('<L', data[offset:offset + bytes_num])
    elif bytes_num == 8:
        data = struct.unpack('<Q', data[offset:offset + bytes_num])
    data = data[0]
    return data, offset + bytes_num


def unpack_double(data, offset):
    data = struct.unpack('<d', data[offset:offset + 8])
    data = data[0]
    return data, offset + 8


def unpack_int(data, offset, bytes_num):
    if bytes_num == 1:
        data = struct.unpack('<b', data[offset:offset + bytes_num])
    elif bytes_num == 2:
        data = struct.unpack('<h', data[offset:offset + bytes_num])
    elif bytes_num == 4:
        data = struct.unpack('<i', data[offset:offset + bytes_num])
    elif bytes_num == 8:
        data = struct.unpack('<q', data[offset:offset + bytes_num])
    data = data[0]
    return data, offset + bytes_num


def unpack_list(data, offset, size, type_size, type_int):
    result = []
    for i in range(size):
        if type_int == 'u':
            result.append(unpack_uint(data, offset, type_size)[0])
            offset = unpack_uint(data, offset, type_size)[1]
        elif type_int == 'i':
            result.append(unpack_int(data, offset, type_size)[0])
            offset = unpack_int(data, offset, type_size)[1]
    return result


def unpack_c_list(data, offset):
    result = []
    size = 4
    for i in range(size):
        result.append(struct_c_parse(data, unpack_uint(data, offset, 4)[0]))
        offset += 4
    return result


def struct_a_parse(data, offset):
    result = {}
    result["A1"], offset = unpack_char(data, offset)
    result["A2"], offset = unpack_uint(data, offset, 4)
    result["A3"], offset = unpack_int(data, offset, 4)
    result["A4"] = struct_b_parse(data, unpack_uint(data, offset, 4)[0])
    offset = unpack_uint(data, offset, 4)[1]
    result["A5"] = struct_d_parse(data, unpack_uint(data, offset, 4)[0])
    return result


def struct_b_parse(data, offset):
    result = {}
    result["B1"] = unpack_c_list(data, offset)
    offset = unpack_uint(data, offset, 4)[1] + 12
    result["B2"] = unpack_uint(data, offset, 4)[0]
    return result


def struct_c_parse(data, offset):
    result = {}
    result["C1"], offset = unpack_double(data, offset)
    result["C2"] = unpack_list(data,
                               unpack_uint(data,
                                           unpack_uint(data,
                                                       offset,
                                                       4)[1],
                                           2)[0],
                               unpack_uint(data, offset, 4)[0], 1, 'i')
    offset = unpack_uint(data, unpack_uint(data, offset, 4)[1], 2)[1]
    result["C3"], offset = unpack_uint(data, offset, 2)
    result["C4"], offset = unpack_uint(data, offset, 8)
    result["C5"] = unpack_list(data,
                               unpack_uint(data,
                                           unpack_uint(data,
                                                       offset,
                                                       4)[1],
                                           2)[0],
                               unpack_uint(data, offset, 4)[0], 1, 'u')
    offset = unpack_uint(data, unpack_uint(data, offset, 4)[1], 2)[1]
    result["C6"], offset = unpack_int(data, offset, 1)
    result["C7"], offset = unpack_int(data, offset, 2)
    return result


def struct_d_parse(data, offset):
    result = {}
    result["D1"], offset = unpack_int(data, offset, 1)
    result["D2"], offset = unpack_int(data, offset, 1)
    result["D3"] = unpack_list(data,
                               unpack_uint(data,
                                           unpack_uint(data,
                                                       offset,
                                                       4)[1],
                                           4)[0],
                               unpack_uint(data, offset, 4)[0], 8, 'u')
    return result


if __name__ == '__main__':
    main((
        b"VKDBfjdWW8\x80\xbcZl\xf2\xb5\x00\x00\x00\xd9\x00\x00\x00\x13qs\xcf\xe8a\xb7\xb9 \xf1\xc2\xbf\x02\x00\x00\x00\x17\x00\t\x87k\xdd\x99\xdc\xcf\x04\xd3\xd9\x02\x00\x00\x00\x19\x00{\xa7\x05oM\xba\x81\x84\xae\x84\xbaKg\t:\xd4?\x02\x00\x00\x00<\x00\x8e\xa8jb\xad\xdf\xd0'\x84Z\x04\x00\x00\x00>\x00a$\xf8\xeaL\xe5\x12\xa0[\x05\xe2l]\xbf\xc8\x0fL\xe3\xbf\x05\x00\x00\x00c\x00|H1\xb4\xda\xaf\xc6\x86m\xf0\x03\x00\x00\x00h\x00\xa1\xf0\xa6\xf1\x97\xe73\xf1\xaby{\x88\xfb4\x85\xb5\xa9\xe2?\x04\x00\x00\x00\x8c\x00{\xf0\xf2\x07\x98\xe2\xb3S8R\x04\x00\x00\x00\x90\x00q\xaeF\x1b\x00\x00\x00B\x00\x00\x00k\x00\x00\x00\x94\x00\x00\x00\xd5\xeb\x8a<\x0byd\xa1,_\xf4z|\xb2\xe4|`b\xf6\x9c\xa5w\x02\x00\x00\x00\xc9\x00\x00\x00"))
