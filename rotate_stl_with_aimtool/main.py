from stl_find_ball                import locate_sphere_in_stl
from solve_rigid_point_set_rt_pro import compute_best_rigid_transform_pro
from stl_scale_translate_rotate   import stl_scale
from stl_scale_translate_rotate   import stl_translate
from stl_scale_translate_rotate   import stl_rotate_quaternion
from rotmat_to_quaternion         import rotation_matrix_to_quaternion
import numpy as np

try:
    from .aimtool_reader import aimtool_reader
except:
    from aimtool_reader import aimtool_reader

def max_min_distance(A: np.ndarray, B: np.ndarray) -> float:
    """
    对 A 中每个点，找到 B 中最近点的距离，返回这些距离的最大值
    
    Args:
        A: np.ndarray, shape (N, 3)
        B: np.ndarray, shape (M, 3)
    
    Returns:
        float: 所有最近距离中的最大值
    """
    # 形状: (N, 1, 3) - (1, M, 3) -> (N, M, 3)
    diff = A[:, None] - B[None, :]
    # 欧氏距离矩阵 (N, M)
    dist = np.sqrt(np.sum(diff ** 2, axis=-1))
    # 每个A点到B的最小距离
    min_dists = dist.min(axis=1)
    # 取最大
    return min_dists.max()

def get_farthest_pair_distance(points: np.ndarray) -> float:
    """
    计算 N * 3 三维点集中最远点对的欧氏距离
    
    Args:
        points: np.ndarray, shape=(N, 3)，三维点集数组
        
    Returns:
        float: 点集中两点之间的最大距离
    """
    # 计算两两之间的欧氏距离矩阵 (N, N)
    diff = points[:, np.newaxis] - points  # 广播计算坐标差
    dist_matrix = np.sqrt(np.sum(diff ** 2, axis=2))  # 距离矩阵
    
    # 取最大值（排除对角线上的0）
    max_dist = np.max(dist_matrix[~np.eye(dist_matrix.shape[0], dtype=bool)])
    
    return max_dist

# 按照 aimtool_path 中的点距离计算
def rotate_stl_with_aimtool(
        stl_path:str, 
        export_path:str, 
        aimtool_path:str) -> float:

    # 找到 STL 文件中的所有标志球
    detected_spheres = locate_sphere_in_stl(stl_path=stl_path)

    # 获取工具中的坐标点集合
    aimtool = aimtool_reader(aimtool_path)

    if len(detected_spheres) != len(aimtool["markers"]):
        raise ValueError("标志球个数不匹配")
    
    # 获得 STL 标志物中心点
    stl_markers = np.array([
        center for center, _ in detected_spheres
    ])

    # 获得 STL 文件中的最远点距离
    fd1 = get_farthest_pair_distance(stl_markers)

    # 获得工具中心点
    aim_markers = np.array(aimtool["markers"])

    # 获得 工具文件中的最远点距离
    fd2 = get_farthest_pair_distance(stl_markers)

    # 对 STL 文件进行缩放
    stl_markers = stl_markers * (fd2 / fd1)
    stl_scale(stl_path, (fd2 / fd1), export_path)

    # 获取旋转平移矩阵
    Rto, Tto = compute_best_rigid_transform_pro(
        stl_markers, aim_markers)
    Rto_l = [
        [float(val) for val in item]
        for item in Rto
    ]
    Tto_l = [float(val) for val in Tto]

    # 旋转平移
    stl_rotate_quaternion(export_path, 
        rotation_matrix_to_quaternion(Rto_l), export_path)
    stl_translate(export_path, Tto_l, export_path)

    # 旋转之后要进行检查
    # 找到 STL 文件中的所有标志球
    new_detected_spheres = locate_sphere_in_stl(export_path)
    new_stl_markers = np.array([
        center for center, _ in new_detected_spheres
    ])

    return float(max_min_distance(
        new_stl_markers, aim_markers))



if __name__ == "__main__":
    print(
        "maximal error for tool",
        rotate_stl_with_aimtool(
            "BONE-1.stl", 
            "BONE-1.new.stl",
            "BONE-2.aimtool"
        )
    )
