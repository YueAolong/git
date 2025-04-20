from PIL import Image
from pathlib import Path
import os
import logging
from datetime import datetime

class ImageResizer:
    def __init__(self, source_dir, max_width=1920):
        # 设置日志
        self.setup_logging()
        
        # 设置参数
        self.source_dir = Path(source_dir)
        self.max_width = max_width
        self.target_dir = self.source_dir / 'resized_images'
        
        # 支持的图片格式
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        
        # 创建目标文件夹
        self.create_target_dir()
    
    def setup_logging(self):
        """设置日志记录"""
        self.logger = logging.getLogger('ImageResizer')
        self.logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        log_file = '图片调整报告.txt'
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def create_target_dir(self):
        """创建目标文件夹"""
        try:
            self.target_dir.mkdir(exist_ok=True)
            self.logger.info(f"创建目标文件夹: {self.target_dir}")
        except Exception as e:
            self.logger.error(f"创建目标文件夹时出错: {e}")
            raise
    
    def resize_image(self, image_path):
        """调整图片大小"""
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 获取原始尺寸
                width, height = img.size
                
                # 如果宽度小于等于最大宽度，则跳过
                if width <= self.max_width:
                    self.logger.info(f"跳过图片 {image_path.name}: 宽度 {width}px 小于等于 {self.max_width}px")
                    return False
                
                # 计算新的高度（保持宽高比）
                new_height = int(height * (self.max_width / width))
                
                # 调整图片大小
                resized_img = img.resize((self.max_width, new_height), Image.Resampling.LANCZOS)
                
                # 保存调整后的图片
                output_path = self.target_dir / image_path.name
                resized_img.save(output_path, quality=95)
                
                self.logger.info(f"调整图片 {image_path.name}: {width}x{height} -> {self.max_width}x{new_height}")
                return True
                
        except Exception as e:
            self.logger.error(f"处理图片 {image_path.name} 时出错: {e}")
            return False
    
    def process_directory(self):
        """处理目录中的所有图片"""
        try:
            # 统计信息
            total_images = 0
            resized_images = 0
            skipped_images = 0
            
            # 遍历源目录中的所有文件
            for file_path in self.source_dir.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in self.image_extensions:
                    total_images += 1
                    if self.resize_image(file_path):
                        resized_images += 1
                    else:
                        skipped_images += 1
            
            # 输出统计信息
            self.logger.info(f"\n处理完成！")
            self.logger.info(f"总图片数: {total_images}")
            self.logger.info(f"已调整: {resized_images}")
            self.logger.info(f"已跳过: {skipped_images}")
            
        except Exception as e:
            self.logger.error(f"处理目录时出错: {e}")
            raise

def main():
    try:
        # 获取用户输入的源目录
        source_dir = input("请输入图片所在文件夹路径: ").strip()
        
        # 创建调整器实例并处理图片
        resizer = ImageResizer(source_dir)
        resizer.process_directory()
        
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main() 