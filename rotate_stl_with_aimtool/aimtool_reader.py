from typing import Any

def aimtool_reader(tool_path: str) -> dict[str, Any]:
    """
    读取并解析 aimtool 工具文件，提取工具名称、标记、标志点坐标与器械尖端向量
    
    Args:
        tool_path: aimtool 文件的路径字符串
    
    Returns:
        包含文件解析结果的字典，结构如下：
            tool_name: 工具名称（文件第一行）
            tool_flag: 工具标记（文件第二行）
            markers: 标志点坐标列表，每个元素为 [x, y, z] 坐标
            tooltip_vec: 器械尖端向量列表，包含两组三维向量
    """
    # 读取文件所有行
    with open(tool_path, "r") as fp:
        lines = list(fp)

    # 获取基本信息
    ans = dict()
    ans["tool_name"] = lines[0].strip()
    ans["tool_flag"] = lines[1].strip()
    ans["markers"] = []

    # 记录所有标志点
    node_cnt = int(lines[2])
    for i in range(node_cnt):
        ans["markers"].append([
            float(item)
            for item in lines[3 + i].split()
        ][:-1])

    # 记录器械尖端
    tip_vec_cnt = int(lines[3 + node_cnt])
    ans["tooltip_vec"] = []
    for i in range(2):
        ans["tooltip_vec"].append([
            float(item)
            for item in lines[3 + node_cnt + 1 + i].split()
        ])

    return ans
    
if __name__ == "__main__":
    print(aimtool_reader("BONE-2.aimtool"))
