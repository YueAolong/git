from pathlib import Path
import shutil
from datetime import datetime
import logging

class FileOrganizer:
    def __init__(self):
        # 设置日志
        self.setup_logging()
        
        # 定义文件类型映射
        self.file_types = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
            'docs': ['.doc', '.docx', '.pdf', '.txt', '.xls', '.xlsx'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz']
        }
        
        # 获取下载文件夹路径
        self.downloads_path = Path.home() / 'Downloads'
        self.logger.info(f"下载文件夹路径: {self.downloads_path}")
        
        # 创建目标文件夹
        self.create_directories()
    
    def setup_logging(self):
        """设置日志记录"""
        self.logger = logging.getLogger('FileOrganizer')
        self.logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        log_file = '文件整理报告.txt'
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
    
    def create_directories(self):
        """创建目标文件夹"""
        try:
            for folder in self.file_types.keys():
                folder_path = self.downloads_path / folder
                folder_path.mkdir(exist_ok=True)
                self.logger.info(f"创建文件夹: {folder_path}")
        except Exception as e:
            self.logger.error(f"创建文件夹时出错: {e}")
            raise
    
    def get_file_category(self, file_path):
        """根据文件扩展名确定文件类别"""
        suffix = file_path.suffix.lower()
        for category, extensions in self.file_types.items():
            if suffix in extensions:
                return category
        return None
    
    def move_file(self, file_path, target_folder):
        """移动文件到目标文件夹"""
        try:
            target_path = target_folder / file_path.name
            if target_path.exists():
                # 如果目标文件已存在，添加时间戳
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                target_path = target_folder / new_name
            
            shutil.move(str(file_path), str(target_path))
            self.logger.info(f"移动文件: {file_path.name} -> {target_path.name}")
            return True
        except Exception as e:
            self.logger.error(f"移动文件 {file_path.name} 时出错: {e}")
            return False
    
    def organize_files(self):
        """整理文件"""
        try:
            # 遍历下载文件夹中的所有文件
            for file_path in self.downloads_path.iterdir():
                if file_path.is_file():
                    category = self.get_file_category(file_path)
                    if category:
                        target_folder = self.downloads_path / category
                        self.move_file(file_path, target_folder)
            
            self.logger.info("文件整理完成")
        except Exception as e:
            self.logger.error(f"整理文件时出错: {e}")
            raise

def main():
    try:
        organizer = FileOrganizer()
        organizer.organize_files()
    except Exception as e:
        print(f"程序执行出错: {e}")

if __name__ == "__main__":
    main() 