import numpy as np
import open3d as o3d
import pyransac3d as pyrsc
import random
def get_angle_vector(a, b, degrees=True):
    """"
    计算法向量的夹角，
    a,b：输入的法向量
    degrees：True输出为角度制，False输出为弧度制。
    """
    cos_a = np.inner(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    if cos_a < -1:
        cos_a = np.array([-1])
    if cos_a > 1:
        cos_a = np.array([1])
    rad = np.arccos(cos_a)  # 计算结果为弧度制
    deg = np.rad2deg(rad)  # 转化为角度制
    angle = deg if degrees else rad
    return angle

def dianyunchazhi(point):
    point.paint_uniform_color([0.5, 0.5, 0.5])  # 把所有点渲染为灰色（灰兔子）
    pcd_tree = o3d.geometry.KDTreeFlann(point)  # 建立KD树索引
    points=np.asarray(point.points)
    len=points.shape[0]
    list=[]
    for i in range(len):
        [k1, idx1, _] = pcd_tree.search_radius_vector_3d(point.points[1], 0.001)  # 半径搜索
        if k1<80:
            for i in range(20):
                x=random.uniform(-0.001,0.001)
                y=random.uniform(-0.001,0.001)
                z=random.uniform(-0.001,0.001)
                nx=points[i][0]+x
                ny=points[i][0]+y
                nz=points[i][0]+z
                list.append([nx,ny,nz])
    add_points=np.asarray(list)
    return np.vstack(points,add_points)


def judge_hanfeng(hanfeng_point):
    xmin,ymin,zmin=np.min(hanfeng_point,axis=0)
    xmax,ymax,zmax=np.max(hanfeng_point,axis=0)
    x=xmax-xmin
    y=ymax-ymin
    z=zmax-zmin
    if x>y:
        if x>z:
            return 0
        else:
            return 2
    else:
        if y>z :
            return 1
        else:
            return 2

def getabc(best_eq1,best_eq2):
    A1,B1,C1,D1=best_eq1
    A2, B2, C2, D2 = best_eq2
    n1=np.asarray([A1,B1,C1])
    n2 = np.asarray([A2, B2, C2])
    n=n1+n2
    cx, cy, cz = n
    l=np.sqrt(cx * cx + cy * cy + cz * cz)

    nl=n/l
    x1,y1,z1=nl
    x=[1,0,0]
    y=[0,1,0]
    z=[0,0,1]
    thetax=np.arccos(x1)
    thetay = np.arccos(y1)
    thetaz = np.arccos(z1)
    return thetax,thetay,thetaz









def hanfengtiqu(point_list,str):
    dx, dy, dz, rx, ry, rz = point_list
    x = rx#-1.535
    y = ry#0.201
    z =rz# -3.097
    dx = dx#0.733564
    dy = dy#-0.319649
    dz =dz# 0.349521
    rx = np.asarray([[1, 0, 0],
                     [0, np.cos(x), -np.sin(x)],
                     [0, np.sin(x), np.cos(x)]])
    ry = np.asarray([[np.cos(y), 0, np.sin(y)],
                     [0, 1, 0],
                     [-np.sin(y), 0, np.cos(y)]])
    rz = np.asarray([[np.cos(z), -np.sin(z), 0],
                     [np.sin(z), np.cos(z), 0],
                     [0, 0, 1]])
    r = np.dot(np.dot(rx, ry), rz)
    # ----------------手眼标定矩阵-------------------------------------35.4816
    R = np.array([[0.140358, 0.741427, -0.65619, 0.050142], [-0.983685, 0.0290993, -0.17753, 0.112442],
                  [-0.112531, 0.670402, 0.733415, -0.346539], [0, 0, 0, 1]])
    # -------------------读取点云数据并可视化------------------------
    pcd_load = o3d.io.read_point_cloud(str)#
    pcd_load.paint_uniform_color([0.5, 0.5, 0.5])
   # o3d.visualization.draw_geometries([pcd_load])
    pcd = pcd_load.voxel_down_sample(voxel_size=0.002)
    #pcd=pcd_load
    # o3d.visualization.draw_geometries([pcd])
    cloud, inds = pcd.remove_radius_outlier(nb_points=20, radius=0.005)
    pcd = pcd.select_by_index(inds)  # .paint_uniform_color([1, 0, 0])
    # o3d.visualization.draw_geometries([pcd])
    points = np.asarray(pcd.points)
    current_point_num = np.shape(points)[0]

    one_points = np.ones((current_point_num, 4))
    one_points[:, 0:3] = points
    tool_point_1 = np.dot(R, one_points.T).T[:, 0:3]

    tool_points = np.dot(r, tool_point_1.T).T + np.asarray([dx, dy, dz])
    tool_point = o3d.geometry.PointCloud()
    tool_point.points = o3d.utility.Vector3dVector(tool_points)

   # o3d.io.write_point_cloud("copy_of_fragment.ply", tool_point)


    # tool_point.paint_uniform_color([0, 0, 0])
  #  o3d.visualization.draw_geometries([tool_point])
    # --------------------RANSAC平面拟合----------------------------
    plano1 = pyrsc.Plane()
    # best_eq：平面方程的系数A、B、C、D，best_inliers：内点，
    # thresh距离阈值， maxIteration：迭代次数
    best_eq1, best_inliers1 = plano1.fit(np.asarray(tool_point.points), thresh=0.001, maxIteration=500)
    # print('平面模型系数为：', best_eq)
    # 获取位于最佳拟合平面上的点
    plane1 = tool_point.select_by_index(best_inliers1)  # .paint_uniform_color([1, 0, 0])
    not_plane = tool_point.select_by_index(best_inliers1, invert=True)  # .paint_uniform_color([0, 1, 0])
    # ncl1, nind1 = not_plane.remove_radius_outlier(nb_points=10, radius=0.005)
    # not_plane=not_plane.select_by_index(nind1)
    # cl1, ind1 = plane1.remove_radius_outlier(nb_points=10, radius=0.005)
    # plane1.select_by_index(ind1)
    plane1.paint_uniform_color([1, 0, 0])
    # 获取平面外的点云
    # planenn=plane.select_by_index(ind, invert=True).paint_uniform_color([0, 0, 1])

    plano2 = pyrsc.Plane()
    # points2 = np.asarray(not_plane.points)
    best_eq2, best_inliers2 = plano2.fit(np.asarray(not_plane.points), thresh=0.001, maxIteration=500)
    plane2 = not_plane.select_by_index(best_inliers2)  # .paint_uniform_color([0, 1, 0])
    not_plane = not_plane.select_by_index(best_inliers2, invert=True)
    plane2.paint_uniform_color([0, 1, 0])
    pcd_tree1 = o3d.geometry.KDTreeFlann(plane1)  # 建立KD树索引
    list1 = []
    plane2_point = np.asarray(plane2.points)
    len = np.asarray(plane2.points).shape[0]
    for i in range(len):
        [k1, idx1, _] = pcd_tree1.search_radius_vector_3d(plane2.points[i],
                                                          0.01)  # 半径搜索.search_hybrid_vector_3d(plane2.points[i], 0.01,2)#
        if k1 > 10:
            list1.append(plane2_point[i])

    hanfeng_point = o3d.geometry.PointCloud()
    hanfeng1 = np.array(list1)
    length1 = hanfeng1.shape[0]
    hanfeng_point.points = o3d.utility.Vector3dVector(hanfeng1)
    hanfeng_point.paint_uniform_color([0, 0, 0])
   # m=judge_hanfeng(np.asarray(hanfeng_point.points))
    #print(m)
  #  o3d.visualization.draw_geometries([hanfeng_point])
    hanfeng_point_xmax = np.sort(hanfeng1[:, 2])[::-1]
    hanfeng_point_xmin = np.sort(hanfeng1[:, 2])
    dian_1 = hanfeng_point_xmax[:10]
    dian_2 = hanfeng_point_xmin[:10]
    A, B, C, D = best_eq1
    d1min = 1000
    d1 = 0
    for i in range(dian_1.shape[0]):
        id = np.where(hanfeng1[:, 2] == dian_1[i])

        x, y, z = hanfeng1[id][0]
        d = np.abs(A * x + B * y + C * z + D) / np.sqrt(A * A + B * B + C * C)
        if d < d1min:
            d1min = d
            d1 = i
            min_dian_1 = hanfeng1[id][0]
    d2min = 1000
    d2 = 0
    for j in range(dian_2.shape[0]):
        id = np.where(hanfeng1[:, 2] == dian_2[j])
        x, y, z = hanfeng1[id][0]
        d = np.abs(A * x + B * y + C * z + D) / np.sqrt(A * A + B * B + C * C)
        if d < d2min:
            d2min = d
            d2 = j
            min_dian_2 = hanfeng1[id][0]
    i = np.where(np.asarray(hanfeng_point.points)[:, 2] == dian_1[d1])
    j = np.where(np.asarray(hanfeng_point.points)[:, 2] == dian_2[d2])
    ii = np.where(np.asarray(plane2.points)[:, 2] == dian_1[d1])
    jj = np.where(np.asarray(plane2.points)[:, 2] == dian_2[d2])

    duandian1 = np.asarray(hanfeng_point.points)[i, :3][0, 0]
    duandian2 = np.asarray(hanfeng_point.points)[j, :3][0, 0]
    plane1.paint_uniform_color([0.5, 0.5, 0.5])
    plane2.paint_uniform_color([0.5, 0.5, 0.5])
    plane2.colors[ii[0]] = [1, 0, 0]
    plane2.colors[jj[0]] = [1, 0, 0]
    pcd_tree2 = o3d.geometry.KDTreeFlann(plane2)  # 建立KD树索引
    list2 = []
    plane1_point = np.asarray(plane1.points)
    len = np.asarray(plane1.points).shape[0]
    for i in range(len):
        [k2, idx2, _] = pcd_tree2.search_radius_vector_3d(plane1.points[i],
                                                          0.01)  # 半径搜索.search_hybrid_vector_3d(plane2.points[i], 0.01,2)#
        if k2 > 10:
            list2.append(plane1_point[i])

    hanfeng_point2 = o3d.geometry.PointCloud()
    hanfeng2 = np.array(list2)
    length2 = hanfeng2.shape[0]
    hanfeng_point2.points = o3d.utility.Vector3dVector(hanfeng2)
    hanfeng_point2.paint_uniform_color([0, 0, 0])
    #m2 = judge_hanfeng(np.asarray(hanfeng_point2.points))
    # print(m)
    #  o3d.visualization.draw_geometries([hanfeng_point])
    hanfeng_point_xmax2 = np.sort(hanfeng2[:, 2])[::-1]
    hanfeng_point_xmin2 = np.sort(hanfeng2[:, 2])
    dian_3 = hanfeng_point_xmax2[:10]
    dian_4 = hanfeng_point_xmin2[:10]
    A, B, C, D = best_eq2
    d3min = 1000
    d3 = 0
    for i in range(dian_3.shape[0]):
        id = np.where(hanfeng2[:, 2] == dian_3[i])

        x, y, z = hanfeng2[id][0]
        d = np.abs(A * x + B * y + C * z + D) / np.sqrt(A * A + B * B + C * C)
        if d < d3min:
            d3min = d
            d3 = i
            min_dian_3 = hanfeng2[id][0]
    d4min = 1000
    d4 = 0
    for j in range(dian_4.shape[0]):
        id = np.where(hanfeng2[:, 2] == dian_4[j])
        x, y, z = hanfeng2[id][0]
        d = np.abs(A * x + B * y + C * z + D) / np.sqrt(A * A + B * B + C * C)
        if d < d4min:
            d4min = d
            d4 = j
            min_dian_4 = hanfeng2[id][0]
    i2 = np.where(np.asarray(hanfeng_point2.points)[:, 2] == dian_3[d3])
    j2 = np.where(np.asarray(hanfeng_point2.points)[:, 2] == dian_4[d4])
    ii2= np.where(np.asarray(plane1.points)[:, 2] == dian_3[d3])
    jj2 = np.where(np.asarray(plane1.points)[:, 2] == dian_4[d4])

    duandian3 = np.asarray(hanfeng_point2.points)[i2, :3][0, 0]
    duandian4 = np.asarray(hanfeng_point2.points)[j2, :3][0, 0]

    #print(duandian1)
  #  print(duandian2)




    plane1.colors[ii2[0]] = [0, 1, 0]
    plane1.colors[jj2[0]] = [0, 1, 0]

  #  print(np.asarray(plane2.points[ii[0]]),np.asarray(plane2.points[jj[0]]))

    xx1,yy1,zz1=duandian1
    xx3, yy3, zz3 = duandian3
    nz=(zz1+zz3)/2
    ll=np.sqrt(np.abs(xx1-xx3)*np.abs(xx1-xx3)+np.abs(yy1-yy3)*np.abs(yy1-yy3))
    if np.abs(xx3)>np.abs((xx1)):
        nx=xx3-ll*np.cos(0.785)
    else:
        nx=xx1-ll*np.cos(0.785)
    if np.abs(yy3)>np.abs((yy1)):
        ny=yy3-ll*np.cos(0.785)
    else:
        ny=yy1-ll*np.cos(0.785)
    new_dian1=np.asarray([nx,ny,nz])
    xx2, yy2, zz2 = duandian2
    xx4, yy4, zz4 = duandian4
    nz2 = (zz4 + zz2) / 2
    ll2 = np.sqrt(np.abs(xx2 - xx4) * np.abs(xx2 - xx4) + np.abs(yy2 - yy4) * np.abs(yy2 - yy4))
    if np.abs(xx2) > np.abs((xx4)):
        nx2 = xx2 - ll2 * np.cos(0.785)
    else:
        nx2 = xx4 - ll2 * np.cos(0.785)
    if np.abs(yy2) > np.abs((yy4)):
        ny2 = yy2 - ll2 * np.cos(0.785)
    else:
        ny2 = yy4 - ll2 * np.cos(0.785)
    new_dian2 = np.asarray([nx2, ny2, nz2])
    duan_dian = np.array([new_dian1,new_dian2])
    duandian = o3d.geometry.PointCloud()
    duandian.points = o3d.utility.Vector3dVector(duan_dian)
    duandian.paint_uniform_color([0, 0, 0])
  #  o3d.visualization.draw_geometries([plane1, plane2,duandian])
    a,b,c=getabc(best_eq1,best_eq2)

    return new_dian1,new_dian2,a,b,c



#0.878632 0.626072 0.149846
#+10 -10 -10
# str=r"D:\develop\python\code\welding_gun_robot\Data\save_point.ply"
# dian1,dian2,A,B,C=hanfengtiqu(2.492,0.353,-2.127,0.829198+0.005,0.478515-0.011,0.163815-0.012,str)#815001
#
# print(dian1,dian2)
# print(A,B,C)
