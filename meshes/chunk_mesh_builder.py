from settings import *
from numba import uint8
from dinary import log_write

@njit
def get_ao(local_pos, world_pos, world_voxels, plane):
    # print("calling get_ao")
    x, y, z = local_pos
    wx, wy, wz = world_pos
    if plane == 'Y':
        a = is_void((x, y, z-1),    (wx, wy, wz-1),     world_voxels)
        b = is_void((x-1, y, z-1),  (wx-1, wy, wz-1),   world_voxels)
        c = is_void((x-1, y, z),    (wx-1, wy, wz),     world_voxels)
        d = is_void((x-1, y, z+1),  (wx-1, wy, wz+1),   world_voxels)
        e = is_void((x, y, z+1),    (wx, wy, wz+1),     world_voxels)
        f = is_void((x+1, y, z+1),  (wx+1, wy, wz+1),   world_voxels)
        g = is_void((x+1, y, z),    (wx+1, wy, wz),     world_voxels)
        h = is_void((x+1, y, z-1),  (wx+1, wy, wz-1),   world_voxels)

    elif plane == 'X':
        a = is_void((x, y, z-1),    (wx, wy, wz-1),     world_voxels)
        b = is_void((x, y-1, z-1),  (wx, wy-1, wz-1),   world_voxels)
        c = is_void((x, y-1, z),    (wx, wy-1, wz),     world_voxels)
        d = is_void((x, y-1, z+1),  (wx, wy-1, wz+1),   world_voxels)
        e = is_void((x, y, z+1),    (wx, wy, wz+1),     world_voxels)
        f = is_void((x, y+1, z+1),  (wx, wy+1, wz+1),   world_voxels)
        g = is_void((x, y+1, z),    (wx, wy+1, wz),     world_voxels)
        h = is_void((x, y+1, z-1),  (wx, wy+1, wz-1),   world_voxels)

    else: # Z plane
        a = is_void((x-1, y, z),    (wx-1, wy, wz),     world_voxels)
        b = is_void((x-1, y-1, z),  (wx-1, wy-1, wz),   world_voxels)
        c = is_void((x, y-1, z),    (wx, wy-1, wz),     world_voxels)
        d = is_void((x+1, y-1, z),  (wx+1, wy-1, wz),   world_voxels)
        e = is_void((x+1, y, z),    (wx+1, wy, wz),     world_voxels)
        f = is_void((x+1, y+1, z),  (wx+1, wy+1, wz),   world_voxels)
        g = is_void((x, y+1, z),    (wx, wy+1, wz),     world_voxels)
        h = is_void((x-1, y+1, z),  (wx-1, wy+1, wz),   world_voxels)
    
    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao

@njit
def to_uint8(x, y, z, voxel_id, face_id, ao_id, flip_id):
    """数据类型不匹配, 用于转换的函数"""
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id), uint8(ao_id), uint8(flip_id)

@njit
def pack_data(x, y, z, voxel_id, face_id, ao_idd, flip_id):
    """打包数据优化显存占用"""
    # print("calling pack_data")
    a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_idd, flip_id
    b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1
    fg_bit = f_bit + g_bit
    efg_bit = e_bit + fg_bit
    defg_bit = d_bit + efg_bit
    cdefg_bit = c_bit + defg_bit
    bcdefg_bit = b_bit + cdefg_bit
    packed_data = \
        a << bcdefg_bit | \
        b << cdefg_bit | \
        c << defg_bit | \
        d << efg_bit | \
        e << fg_bit | \
        f << g_bit | \
        g
    return packed_data

@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels):
    """判断是非为空块"""
    # print("is_void")
    chunk_index = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        return False
    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_voxel_pos
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA
    voxel_id = chunk_voxels[voxel_index]
    if voxel_id != 0:
        if voxel_id & 128 == 0:
            return False
    return True

@njit
def add_data(vertex_data, index, *vertices):
    # print("add_data")
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index

@njit
def add_packed_data(vertex_data, index, *vertices):
    """添加打包后的数据"""
    # print("calling add_packed_data")
    for vertex in vertices:
        vertex_data[index] = vertex
        index += 1
    return index

@log_write(message="build_chunck_mesh")
@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, word_voxels):
    
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype=np.uint32)
    index = 0

    # test begin
    # count = 1
    # max_index = 0
    # test end

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                # test begin
                # index_tmp = x + CHUNK_SIZE * z + CHUNK_AREA * y
                # max_index = max_index if max_index > index_tmp else index_tmp
                # test_flg = True if index_tmp == 21937 else False
                # if test_flg:
                #     print(count, x, y, z, max_index, index_tmp)
                # count += 1
                # test end

                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                # print("valid index, get data successfully !")
                if voxel_id == 0:
                    continue

                # 判断是否为透明方块
                flip_id = 1 if voxel_id & 128 != 0 else 0
                if flip_id:
                    voxel_id = ~ voxel_id + 1
                    
                # 计算小方块在世界坐标系中的位置
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # test begin
                # if test_flg:
                #     print("第一次调用 is_void, 计算顶面")
                # test end

                # 通过定义每个面的顶点坐标位置及属性来构建数组
                # 数据格式： x, y, z, voxel_id, face_id
                # 顶面
                if is_void((x, y + 1, z), (wx, wy + 1, wz), word_voxels):

                    # if test_flg:
                    #     print("is_void 调用一切正常, 开始调用 get_vao")

                    ao = get_ao((x, y+1, z), (wx, wy+1, wz), word_voxels, plane='Y')

                    # if test_flg:
                    #     print("get_ao 调用一切正常, 开始数据打包")

                    v0 = pack_data(x, y+1, z, voxel_id, 0, ao[0], flip_id)
                    v1 = pack_data(x+1, y+1, z, voxel_id, 0, ao[1], flip_id)
                    v2 = pack_data(x+1, y+1, z+1, voxel_id, 0, ao[2], flip_id)
                    v3 = pack_data(x, y+1, z+1, voxel_id, 0, ao[3], flip_id)

                    # if test_flg:
                    #     print("数据打包一切正常, 开始写入数据")

                    index =  add_packed_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                    # if test_flg:
                    #     print("数据写入正常， over")
                    
                # test begin
                # if test_flg:
                #     print("第二次调用 is_void, 计算底面")
                # test end

                # 底面
                if is_void((x, y - 1, z), (wx, wy - 1, wz), word_voxels):
                    ao = get_ao((x, y-1, z), (wx, wy-1, wz), word_voxels, plane='Y')
                    
                    v0 = pack_data(x, y, z, voxel_id, 1, ao[0], flip_id)
                    v1 = pack_data(x+1, y, z, voxel_id, 1, ao[1], flip_id)
                    v2 = pack_data(x+1, y, z+1, voxel_id, 1, ao[2], flip_id)
                    v3 = pack_data(x, y, z+1, voxel_id, 1, ao[3], flip_id)

                    index = add_packed_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # test begin
                # if test_flg:
                #     print("第三次调用 is_void, 计算右面")
                # test end

                # 右面
                if is_void((x + 1, y, z), (wx + 1, wy, wz), word_voxels):
                    ao = get_ao((x+1, y, z), (wx+1, wy, wz), word_voxels, plane='X')

                    v0 = pack_data(x+1, y, z, voxel_id, 2, ao[0], flip_id)
                    v1 = pack_data(x+1, y+1, z, voxel_id, 2, ao[1], flip_id)
                    v2 = pack_data(x+1, y+1, z+1, voxel_id, 2, ao[2], flip_id)
                    v3 = pack_data(x+1, y, z+1, voxel_id, 2, ao[3], flip_id)

                    index = add_packed_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # test begin
                # if test_flg:
                #     print("第四次调用 is_void, 计算左面")
                # test end

                # 左面
                if is_void((x - 1, y, z), (wx - 1, wy, wz), word_voxels):
                    ao = get_ao((x-1, y, z), (wx-1, wy, wz), word_voxels, plane='X')

                    v0 = pack_data(x, y, z, voxel_id, 3, ao[0], flip_id)
                    v1 = pack_data(x, y+1, z, voxel_id, 3, ao[1], flip_id)
                    v2 = pack_data(x, y+1, z+1, voxel_id, 3, ao[2], flip_id)
                    v3 = pack_data(x, y, z+1, voxel_id, 3, ao[3], flip_id)

                    index = add_packed_data(vertex_data, index, v0, v2, v1, v0, v3, v2)


                # test begin
                # if test_flg:
                #     print("第五次调用 is_void, 计算后面")
                # test end
                
                # 后面
                if is_void((x, y, z - 1), (wx , wy, wz - 1), word_voxels):
                    ao = get_ao((x, y, z-1), (wx, wy, wz-1), word_voxels, plane='Z')

                    v0 = pack_data(x, y, z, voxel_id, 4, ao[0], flip_id)
                    v1 = pack_data(x, y+1, z, voxel_id, 4, ao[1], flip_id)
                    v2 = pack_data(x+1, y+1, z, voxel_id, 4, ao[2], flip_id)
                    v3 = pack_data(x+1, y, z, voxel_id, 4, ao[3], flip_id)

                    index = add_packed_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # test begin
                # if test_flg:
                #     print("第六次调用 is_void, 计算前面")
                # test end

                # 前面
                if is_void((x, y, z + 1), (wx, wy, wz + 1), word_voxels):
                    ao = get_ao((x, y, z+1), (wx, wy, wz+1), word_voxels, plane='Z')

                    v0 = pack_data(x, y, z+1, voxel_id, 5, ao[0], flip_id)
                    v1 = pack_data(x, y+1, z+1, voxel_id, 5, ao[1], flip_id)
                    v2 = pack_data(x+1, y+1, z+1, voxel_id, 5, ao[2], flip_id)
                    v3 = pack_data(x+1, y, z+1, voxel_id, 5, ao[3], flip_id)

                    index = add_packed_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
    return vertex_data[:index]

@njit
def get_chunk_index(world_voxel_pos):
    """获取chunk的索引"""
    # print("calling get_chunk_index")
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
        index = cx + WORLD_D * cz + WORLD_AREA * cy
        return index
    return -1