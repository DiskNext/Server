"""
Pytest配置文件
"""
import pytest
import os
import sys

# 添加项目根目录到Python路径，确保可以导入项目模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
