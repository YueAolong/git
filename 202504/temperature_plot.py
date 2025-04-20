import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # 放在最上面
# 创建图形和 canvas 对象
fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvas(fig)  # 绑定 Figure 到 canvas

# 添加子图
ax = fig.add_subplot(111)
ax.plot([1, 2, 3], [4, 5, 6])

# 渲染图像
canvas.draw()

# ----------------------------
# 关键修改点：使用 buffer_rgba() 获取 RGBA 数据
# ----------------------------
rgba_data = canvas.buffer_rgba()  # 获取 RGBA 格式数据
width, height = canvas.get_width_height()

# 转换为 numpy array（直接使用 buffer_rgba 的接口）
image = np.asarray(rgba_data).reshape(height, width, 4)

# 提取 RGB 通道（RGBA -> RGB）
image_rgb = image[..., :3]  # 直接取前 3 个通道（R, G, B）

# 展示图像（注意通道顺序已经是 RGB）
plt.imshow(image_rgb)
plt.axis('off')
plt.show()