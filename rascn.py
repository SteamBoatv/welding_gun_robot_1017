import numpy as np
import open3d as o3d
import pyransac3d as pyrsc

DE_BUG = 0
POINT_MAX = None
POINT_MIN = None


def ransac_line_fitting(point_cloud):
    np_points = np.asarray(point_cloud.points)
    line = pyrsc.Line()
    A, B, inliers = line.fit(np_points, thresh=0.001, maxIteration=2000)  # np_points, 内点阈值, 最大迭代次数
    points = point_cloud.select_by_index(inliers)

    best_line_cut = truncate_line_with_point_cloud(A, B, points)

    return best_line_cut


def truncate_line_with_point_cloud(direction_vector, point_on_line, points):
    def line_equation(t):
        return point_on_line + direction_vector * t

    points = np.asarray(points.points)
    # 计算点云在直线方向上的投影参数 t
    t_values = np.dot(points - point_on_line, direction_vector) / np.dot(direction_vector, direction_vector)

    # 找到投影参数的最小和最大值，即线段的端点
    t_min = np.min(t_values)
    t_max = np.max(t_values)

    # 计算线段的起点和终点
    point_min = line_equation(t_min)
    point_max = line_equation(t_max)

    return point_min, point_max


# 拐点判断
def extract_change_points(point_cloud, threshold_angle, knn):  # 点云集合 阈值角度 搜索范围
    change_points = o3d.geometry.PointCloud()
    # change_points.points = o3d.utility.Vector3dVector([point_cloud.points[0]])  # 初始点默认为突变点
    num_points = len(point_cloud.points)

    kd_tree = o3d.geometry.KDTreeFlann(point_cloud)
    for i in range(1, num_points):
        current_point = point_cloud.points[i]
        # 在指定半径内搜索临近点
        # [k, idx, _] = kd_tree.search_radius_vector_3d(current_point, 0.005)
        # 提取临近点的法向量并归一化
        [k, idx, _] = kd_tree.search_knn_vector_3d(current_point, knn)
        neighbor_normals = []
        for index in idx:
            neighbor_normals.append(point_cloud.normals[index])
        neighbor_normals = np.asarray(neighbor_normals)
        neighbor_normals /= np.linalg.norm(neighbor_normals, axis=1, keepdims=True)
        # neighbor_normals:满足这个函数的点kd_tree.search_knn_vector_3d(current_point,knn)
        # 计算当前点与临近点法向量的夹角
        # 求内积
        dot_products = np.dot(neighbor_normals, point_cloud.normals[i])
        # 绝对值
        dot_products = np.abs(dot_products)
        angles = np.arccos(np.clip(dot_products, -1.0, 1.0))
        # 判断是否为突变点
        if np.mean(angles) > threshold_angle:
            change_points.points.append(current_point)

        # FLAG = True
        # for angle in angles:
        #     if angle < threshold_angle:
        #         FLAG = False
        # if FLAG:
        #     change_points.points.append(point_cloud.points[i])

    return change_points


# 线性插值
def interpolate_points(point_min, point_max, num_points=21):
    # 计算间隔
    interval = 1.0 / (num_points - 1)

    # 初始化插值点列表
    interpolated_points = []

    # 使用线性插值生成新的点
    for i in range(num_points):
        t = i * interval
        interpolated_point = point_min + t * (point_max - point_min)
        interpolated_points.append(interpolated_point)

    # 转换为PointCloud数据类型
    pcd_between = o3d.geometry.PointCloud()
    pcd_between.points = o3d.utility.Vector3dVector(interpolated_points)
    return pcd_between


def fit_intersection_line(hanfeng_point):
    # L形状 hanfeng_point
    # 去除离群点 计算法线，搜索半径0.01cm，只考虑邻域内的20个点
    cloud, inds = hanfeng_point.remove_radius_outlier(nb_points=50, radius=0.005)
    hanfeng_point = hanfeng_point.select_by_index(inds)
    if DE_BUG:
        o3d.visualization.draw_geometries([hanfeng_point], window_name='拐角')

    # 计算法线，搜索半径0.01cm，只考虑邻域内的10个点
    hanfeng_point.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=10))

    # 设置点云颜色
    hanfeng_point.paint_uniform_color([0.0, 1.0, 0.0])
    if DE_BUG:
        o3d.visualization.draw_geometries([hanfeng_point], point_show_normal=True, window_name='拐角带线')

    # ----------------提取焊缝-------------------------------------
    hanfeng = extract_change_points(hanfeng_point, 0.4, 10)  # 判断突变 阈值 搜索半径

    hanfeng.paint_uniform_color([1.0, 0.0, 0.0])

    if DE_BUG:
        o3d.visualization.draw_geometries([hanfeng], window_name='提取完的焊缝')
        o3d.visualization.draw_geometries([hanfeng, hanfeng_point], window_name='提取完的焊缝+L形拐角')

    # ----------------拟合直线-------------------------------------
    # 将点拟合成一条直线
    point_min, point_max = ransac_line_fitting(hanfeng)
    if point_max[2] > point_min[2]:
        pass
    else:
        temp = point_min
        point_min = point_max
        point_max = temp
    print("POINT_MIN,POINT_MAX is:")
    print(point_min * 1000, point_max * 1000)
    global POINT_MAX
    POINT_MAX = point_max * 1000
    global POINT_MIN
    POINT_MIN = point_min * 1000

    points_between = interpolate_points(point_min, point_max, num_points=21)
    points_between.paint_uniform_color([1, 0, 1])
    # 创建线段几何对象
    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector([point_min, point_max])
    line_set.lines = o3d.utility.Vector2iVector([[0, 1]])
    line_set.paint_uniform_color([1, 0, 0])  # 设置线段的颜色
    if DE_BUG:
        o3d.visualization.draw_geometries([hanfeng_point, line_set, points_between], window_name='提取到的焊缝结果+L形')

    return points_between, line_set


def interpolate_point_cloud(point_cloud, target_num_points):
    point_cloud_array2 = np.asarray(point_cloud.points)
    num_points = point_cloud_array2.shape[0]

    if num_points == target_num_points:
        return point_cloud

    indices = np.random.choice(num_points, target_num_points, replace=True)
    interpolated_points = np.asarray(point_cloud.points)[indices]

    interpolated_point_cloud = o3d.geometry.PointCloud()
    interpolated_point_cloud.points = o3d.utility.Vector3dVector(interpolated_points)

    return interpolated_point_cloud


def hanfengtiqu(point_list, str):
    dx, dy, dz, A, B, C = point_list
    dx = dx / 1000
    dy = dy / 1000
    dz = dz / 1000
    A = (A / 180) * 3.14
    B = (B / 180) * 3.14
    C = (C / 180) * 3.14
    x = A  # -1.535
    y = B  # 0.201
    z = C  # -3.097
    # dx 变成m
    # x,y,z变成弧度
    rx = np.asarray([[1, 0, 0],
                     [0, np.cos(x), -np.sin(x)],
                     [0, np.sin(x), np.cos(x)]])
    ry = np.asarray([[np.cos(y), 0, np.sin(y)],
                     [0, 1, 0],
                     [-np.sin(y), 0, np.cos(y)]])
    rz = np.asarray([[np.cos(z), -np.sin(z), 0],
                     [np.sin(z), np.cos(z), 0],
                     [0, 0, 1]])
    r = np.dot(np.dot(rz, ry), rx)
    tool_offset = np.array([dx, dy, dz])
    # ----------------手眼标定矩阵-------------------------------------35.4816
    R = np.array([[-0.000227347, -0.999985, -0.00543129, 0.228356], [0.983087, -0.00121817, 0.183133, -0.0855676],
                  [-0.183136, -0.0052978, 0.983073, -0.327596], [0, 0, 0, 1]])
    R_rotation = R[:3, :3]
    R_offset = R[:3, 3]

    # -------------------读取点云数据并可视化------------------------
    pcd_load = o3d.io.read_point_cloud(str)
    pcd_load.paint_uniform_color([0.5, 0.5, 0.5])
    pcd = pcd_load.voxel_down_sample(voxel_size=0.001)  # 下采样体素间距
    cloud, inds = pcd.remove_radius_outlier(nb_points=20, radius=0.005)
    pcd = pcd.select_by_index(inds)  # .paint_uniform_color([1, 0, 0])

    # 坐标转换
    tool_point = np.dot(R_rotation, np.asarray(pcd.points).T).T + R_offset
    base_point = np.dot(r, tool_point.T).T + tool_offset
    base_point_cloud = o3d.geometry.PointCloud()
    base_point_cloud.points = o3d.utility.Vector3dVector(base_point)
    if DE_BUG:
        o3d.visualization.draw_geometries([base_point_cloud], window_name='总览')

    # --------------------底部去除-----------------------------------
    # 设置 Z 轴阈值
    z_threshold = -0.4
    # 筛选出 Z 轴较大的点
    filtered_points = [
        point for point in base_point if point[2] >= z_threshold]
    # 创建一个新的点云对象并设置筛选后的点
    base_point_cloud = o3d.geometry.PointCloud()
    base_point_cloud.points = o3d.utility.Vector3dVector(filtered_points)
    if DE_BUG:
        o3d.visualization.draw_geometries([base_point_cloud], window_name='底部去除')

    # --------------------RANSAC平面拟合----------------------------
    plano1 = pyrsc.Plane()
    # best_eq：平面方程的系数A、B、C、D，best_inliers：内点，
    # thresh距离阈值， maxIteration：迭代次数
    best_eq1, best_inliers1 = plano1.fit(np.asarray(base_point_cloud.points), thresh=0.0005, maxIteration=1000)
    # print('平面模型系数为：', best_eq)
    # 获取位于最佳拟合平面上的点
    plane1 = base_point_cloud.select_by_index(best_inliers1)  # .paint_uniform_color([1, 0, 0])
    not_plane = base_point_cloud.select_by_index(best_inliers1, invert=True)  # .paint_uniform_color([0, 1, 0])
    if DE_BUG:
        o3d.visualization.draw_geometries([not_plane], window_name='A面以外')

    plane1.paint_uniform_color([1, 0, 0])
    if DE_BUG:
        o3d.visualization.draw_geometries([plane1], window_name='A面')

    plano2 = pyrsc.Plane()
    best_eq2, best_inliers2 = plano2.fit(np.asarray(not_plane.points), thresh=0.0005, maxIteration=1000)
    plane2 = not_plane.select_by_index(best_inliers2)  # .paint_uniform_color([0, 1, 0])
    not_plane = not_plane.select_by_index(best_inliers2, invert=True)
    plane2.paint_uniform_color([0, 1, 0])
    if DE_BUG:
        o3d.visualization.draw_geometries([plane2], window_name='B面')
    # --------------------平面1边缘提取----------------------------
    pcd_tree1 = o3d.geometry.KDTreeFlann(plane1)  # 建立KD树索引 kd
    list1 = []
    plane2_point = np.asarray(plane2.points)
    len = np.asarray(plane2.points).shape[0]
    for i in range(len):
        [k1, idx1, _] = pcd_tree1.search_radius_vector_3d(plane2.points[i],
                                                          0.01)
        if k1 > 10:
            list1.append(plane2_point[i])

    hanfeng_point1 = o3d.geometry.PointCloud()
    hanfeng1 = np.array(list1)

    hanfeng_point1.points = o3d.utility.Vector3dVector(hanfeng1)
    hanfeng_point1.paint_uniform_color([0, 0, 0])

    # --------------------平面2边缘提取----------------------------
    pcd_tree2 = o3d.geometry.KDTreeFlann(plane2)  # 建立KD树索引
    list2 = []
    plane1_point = np.asarray(plane1.points)
    len = np.asarray(plane1.points).shape[0]
    for i in range(len):
        [k2, idx2, _] = pcd_tree2.search_radius_vector_3d(plane1.points[i],
                                                          0.01)
        if k2 > 10:
            list2.append(plane1_point[i])

    hanfeng_point2 = o3d.geometry.PointCloud()
    hanfeng2 = np.array(list2)

    hanfeng_point2.points = o3d.utility.Vector3dVector(hanfeng2)

    base_point_cloud.paint_uniform_color([0.5, 0.5, 0.5])
    hanfeng_point2.paint_uniform_color([0, 0, 0])
    plane2.paint_uniform_color([0, 1, 0])
    if DE_BUG:
        o3d.visualization.draw_geometries([hanfeng_point2], window_name='hanfeng——point2')
        o3d.visualization.draw_geometries([base_point_cloud, plane2, hanfeng_point2], window_name='hanfeng_pointJ')

    # 平面拼接
    hanfeng_point = hanfeng_point1 + hanfeng_point2
    # 直线提取
    points_between, line_set = fit_intersection_line(hanfeng_point)
    # 创建坐标轴的模型
    axis_mesh = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.5)
    if DE_BUG:
        o3d.visualization.draw_geometries([base_point_cloud, line_set, axis_mesh], window_name='hanfeng_pointK')

    return points_between


str = r"./Data/save_point.ply"


def point_cal(nums):
    # [dx, dy, dz, A, B, C] = [1280.577, -471.799, -211.454, -170.650, -43.845, 29.179]
    hanfengtiqu(nums, str)  # 815001
    print("in point_cal :")
    global POINT_MAX
    global POINT_MIN
    print(POINT_MAX, POINT_MIN)
    return POINT_MAX, POINT_MIN
