import numpy as np
import matplotlib.pyplot as plt

# ノードAの座標 (絶対位置)
node_a_position = np.array([0, 0])

# ノードBの座標 (未知の値)
node_b_position = np.array([5, 2])

# ノードCの座標 (未知の値)
node_c_position = np.array([2, 5])

# ノードDの本当の座標 (真値)
true_node_d_position = np.array([7, 7])

# UWBによる距離と角度のシミュレーション関数
def simulate_uwb_measurement(reference_node, target_node, distance_stddev=0.1, angle_stddev=np.radians(1)):
    distance = np.linalg.norm(target_node - reference_node)
    angle = np.arctan2(target_node[1] - reference_node[1], target_node[0] - reference_node[0])
    
    distance += np.random.normal(scale=distance_stddev)
    angle += np.random.normal(scale=angle_stddev)
    
    return distance, angle

# ノードCはノードAのUWBによる距離と角度から位置を推定
distance_c, angle_c = simulate_uwb_measurement(node_a_position, node_c_position)
estimated_node_c_position = node_a_position + np.array([distance_c * np.cos(angle_c), distance_c * np.sin(angle_c)])

# ノードBも同様にノードAのUWBによる距離と角度から位置を推定
distance_b, angle_b = simulate_uwb_measurement(node_a_position, node_b_position)
estimated_node_b_position = node_a_position + np.array([distance_b * np.cos(angle_b), distance_b * np.sin(angle_b)])

# ノードDはノードCとノードBの位置からUWBによる角度と距離を計算して算出
vector_cd = estimated_node_c_position - node_a_position
vector_bd = estimated_node_b_position - node_a_position

# ノードCからのUWBによる角度と距離
angle_cd = np.arctan2(vector_cd[1], vector_cd[0])
distance_cd = np.linalg.norm(vector_cd)

# ノードBからのUWBによる角度と距離
angle_bd = np.arctan2(vector_bd[1], vector_bd[0])
distance_bd = np.linalg.norm(vector_bd)

# ベクトル合成してノードDの位置を計算
vector_ad = np.array([distance_cd * np.cos(angle_cd) + distance_bd * np.cos(angle_bd),
                      distance_cd * np.sin(angle_cd) + distance_bd * np.sin(angle_bd)])
estimated_node_d_position = node_a_position + vector_ad

# 結果の表示
print(f"Node Cの推定位置: {estimated_node_c_position}")
print(f"Node Bの推定位置: {estimated_node_b_position}")
print(f"Node Dの推定位置: {estimated_node_d_position}")

# ノードDの本当の座標と推定した座標の比較
print(f"\nNode Dの本当の座標: {true_node_d_position}")
print(f"Node Dの推定した座標: {estimated_node_d_position}")

# 誤差の計算
error_d = np.linalg.norm(true_node_d_position - estimated_node_d_position)
print(f"\n推定誤差 (Dの情報を使用): {error_d}")

# グラフにプロット
plt.figure(figsize=(10, 10))
plt.scatter(*node_a_position, label='Node A ', marker='o', color='red', s=100)
plt.scatter(*node_b_position, label='Node B ', marker='o', color='blue', s=100)
plt.scatter(*node_c_position, label='Node C ', marker='o', color='green', s=100)
plt.scatter(*true_node_d_position, label='Node D ', marker='o', color='purple', s=100)
plt.scatter(*estimated_node_b_position, label='Node B Estimate', marker='x', color='blue', s=100)
plt.scatter(*estimated_node_c_position, label='Node C Estimate', marker='x', color='green', s=100)
plt.scatter(*estimated_node_d_position, label='Node D Estimate', marker='x', color='purple', s=100)


# プロットの設定
plt.title('Node Positions and Estimates',fontsize=25)
plt.xlabel('X coordinates',fontsize=25)
plt.ylabel('Y coordinates',fontsize=25)
plt.legend(fontsize=24)
plt.grid(True)

# グラフを表示
plt.show()
