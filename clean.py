import os
import shutil
from pkg.log import log as log
import argparse
from typing import List, Tuple, Set
import time

Version = "2.1.0"

# 默认排除的目录
DEFAULT_EXCLUDE_DIRS = {"venv", "env", ".venv", ".env", "node_modules"}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='清理 Python 缓存文件')
    parser.add_argument('-p', '--path', default=os.getcwd(),
                       help='要清理的目录路径，默认为当前工作目录')
    parser.add_argument('-y', '--yes', action='store_true',
                       help='自动确认所有操作，不再询问')
    parser.add_argument('--no-pycache', action='store_true',
                       help='不清理 __pycache__ 目录')
    parser.add_argument('--no-nicegui', action='store_true',
                       help='不清理 .nicegui 目录')
    parser.add_argument('--no-testdb', action='store_true',
                       help='不清理 test.db 文件')
    parser.add_argument('--pyc', action='store_true',
                       help='清理 .pyc 文件')
    parser.add_argument('--pytest-cache', action='store_true',
                       help='清理 .pytest_cache 目录')
    parser.add_argument('--exclude', type=str, default="",
                       help='排除的目录，多个目录用逗号分隔')
    parser.add_argument('--log-file', 
                       help='指定日志文件路径')
    parser.add_argument('--dry-run', action='store_true',
                       help='仅列出将要删除的文件，不实际删除')
    return parser.parse_args()

def confirm_action(message: str, auto_yes: str = False) -> bool:
    if auto_yes:
        return True
    return input(f"{message} (y/N): ").lower() == 'y'

def safe_remove(path: str, dry_run: bool = False) -> Tuple[bool, str]:
    """安全删除文件或目录"""
    try:
        if dry_run:
            return True, f"DRY RUN: 将删除 {path}"
        
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        return True, ""
    except PermissionError as e:
        return False, f"权限错误: {e}"
    except OSError as e:
        return False, f"系统错误: {e}"
    except Exception as e:
        return False, f"未知错误: {e}"

def get_excluded_dirs(exclude_arg: str) -> Set[str]:
    """获取要排除的目录列表"""
    result = set(DEFAULT_EXCLUDE_DIRS)
    if exclude_arg:
        for item in exclude_arg.split(','):
            item = item.strip()
            if item:
                result.add(item)
    return result

def clean_pycache(root_dir: str, exclude_dirs: Set[str], dry_run: bool = False) -> List[str]:
    """清理 __pycache__ 目录"""
    log.info("开始清理 __pycache__ 目录...")
    cleaned_paths = []
    
    for dirpath, dirnames, _ in os.walk(root_dir):
        # 排除指定目录
        for exclude in exclude_dirs:
            if exclude in dirnames:
                dirnames.remove(exclude)
        
        if "__pycache__" in dirnames:
            pycache_dir = os.path.join(dirpath, "__pycache__")
            success, error = safe_remove(pycache_dir, dry_run)
            if success:
                cleaned_paths.append(pycache_dir)
            else:
                log.error(f"无法清理 {pycache_dir}: {error}")
    
    return cleaned_paths

def clean_pyc_files(root_dir: str, exclude_dirs: Set[str], dry_run: bool = False) -> List[str]:
    """清理 .pyc 文件"""
    log.info("开始清理 .pyc 文件...")
    cleaned_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 排除指定目录
        for exclude in exclude_dirs:
            if exclude in dirnames:
                dirnames.remove(exclude)
        
        for filename in filenames:
            if filename.endswith('.pyc'):
                file_path = os.path.join(dirpath, filename)
                success, error = safe_remove(file_path, dry_run)
                if success:
                    cleaned_files.append(file_path)
                else:
                    log.error(f"无法清理 {file_path}: {error}")
    
    return cleaned_files

def clean_pytest_cache(root_dir: str, exclude_dirs: Set[str], dry_run: bool = False) -> List[str]:
    """清理 .pytest_cache 目录"""
    log.info("开始清理 .pytest_cache 目录...")
    cleaned_paths = []
    
    for dirpath, dirnames, _ in os.walk(root_dir):
        # 排除指定目录
        for exclude in exclude_dirs:
            if exclude in dirnames:
                dirnames.remove(exclude)
        
        if ".pytest_cache" in dirnames:
            cache_dir = os.path.join(dirpath, ".pytest_cache")
            success, error = safe_remove(cache_dir, dry_run)
            if success:
                cleaned_paths.append(cache_dir)
            else:
                log.error(f"无法清理 {cache_dir}: {error}")
    
    return cleaned_paths

def clean_nicegui(root_dir: str, dry_run: bool = False) -> Tuple[bool, str]:
    """清理 .nicegui 目录"""
    log.info("开始清理 .nicegui 目录...")
    nicegui_dir = os.path.join(root_dir, ".nicegui")
    if os.path.exists(nicegui_dir) and os.path.isdir(nicegui_dir):
        success, error = safe_remove(nicegui_dir, dry_run)
        if success:
            return True, nicegui_dir
        else:
            log.error(f"无法清理 {nicegui_dir}: {error}")
            return False, nicegui_dir
    return False, nicegui_dir

def clean_testdb(root_dir: str, dry_run: bool = False) -> Tuple[bool, str, str]:
    """清理测试数据库文件"""
    log.info("开始清理 test.db 文件...")
    test_db = os.path.join(root_dir, "test.db")
    if os.path.exists(test_db) and os.path.isfile(test_db):
        success, error = safe_remove(test_db, dry_run)
        if success:
            return True, test_db, ""
        else:
            return False, test_db, error
    return False, test_db, "文件不存在"

def main():
    start_time = time.time()
    args = parse_args()
    root_dir = os.path.abspath(args.path)
    exclude_dirs = get_excluded_dirs(args.exclude)

    # 设置日志文件
    if args.log_file:
        log.set_log_file(args.log_file)

    log.title()
    log.title(title=f"清理工具 Cleaner\t\tVersion:{Version}", size="h2")
    print('')

    if not os.path.exists(root_dir):
        log.error(f"目录不存在 Directory not exists: {root_dir}")
        return 1

    log.info(f"清理目录 Clean Directory: {root_dir}")
    if args.dry_run:
        log.warning("模拟运行模式: 将只列出要删除的文件，不会实际删除")
    
    if exclude_dirs:
        log.info(f"排除目录: {', '.join(exclude_dirs)}")

    try:
        total_cleaned = 0
        
        # 清理 __pycache__
        if not args.no_pycache and confirm_action("是否清理 __pycache__ 目录?", args.yes):
            cleaned = clean_pycache(root_dir, exclude_dirs, args.dry_run)
            for path in cleaned:
                log.info(f"已清理 Removed: {path}")
            total_cleaned += len(cleaned)

        # 清理 .pyc 文件
        if args.pyc and confirm_action("是否清理 .pyc 文件?", args.yes):
            cleaned = clean_pyc_files(root_dir, exclude_dirs, args.dry_run)
            for path in cleaned:
                log.info(f"已清理 Removed: {path}")
            total_cleaned += len(cleaned)
            
        # 清理 .pytest_cache
        if args.pytest_cache and confirm_action("是否清理 .pytest_cache 目录?", args.yes):
            cleaned = clean_pytest_cache(root_dir, exclude_dirs, args.dry_run)
            for path in cleaned:
                log.info(f"已清理 Removed: {path}")
            total_cleaned += len(cleaned)

        # 清理 .nicegui
        if not args.no_nicegui and confirm_action("是否清理 .nicegui 目录?", args.yes):
            cleaned, path = clean_nicegui(root_dir, args.dry_run)
            if cleaned:
                log.info(f"已清理 Removed: {path}")
                total_cleaned += 1
            else:
                log.debug(f"未找到 Not found: {path}")

        # 清理 test.db
        if not args.no_testdb and confirm_action("是否清理 test.db 文件?", args.yes):
            success, path, error = clean_testdb(root_dir, args.dry_run)
            if success:
                log.info(f"已清理 Removed: {path}")
                total_cleaned += 1
            elif error == "文件不存在":
                log.debug(f"未找到 Not found: {path}")
            else:
                log.error(f"清理失败 Failed: {error}")

    except KeyboardInterrupt:
        log.warning("操作被用户中断")
        return 1
    except Exception as e:
        log.error(f"错误 Error: {e}")
        return 1
    else:
        elapsed_time = time.time() - start_time
        if args.dry_run:
            log.success(f"模拟清理结束，发现 {total_cleaned} 个可清理项目 (用时: {elapsed_time:.2f}秒)")
        else:
            log.success(f"清理结束，共清理 {total_cleaned} 个项目 (用时: {elapsed_time:.2f}秒)")
        return 0

if __name__ == "__main__":
    exit(main())