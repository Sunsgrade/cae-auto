import os
"""
删除绝对路径下，后缀不符合的文件。相对目录是程序当前命令行所在的目录。所以要用绝对目录，避免出现问题。


"""
def safe_clean_files(target_dir, allowed_extensions):
    """严格限定仅删除 target_dir 目录内的文件（不含子目录）"""
    target_dir = os.path.abspath(target_dir)
    print(f"安全模式清理目录：{target_dir}")

    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)
        
        # 双重保险：确认文件在目标目录内且是普通文件
        if not os.path.isfile(filepath):
            continue  # 跳过目录/链接等
        if not os.path.abspath(filepath).startswith(target_dir):
            print(f"安全拦截：外部文件 {filepath}")
            continue

        ext = os.path.splitext(filename)[1].lower()
        if ext not in allowed_extensions:
            try:
                os.remove(filepath)
                print(f'已删除：{filepath}')
            except Exception as e:
                print(f"删除失败 {filename}，原因：{e}")

# 使用示例
target_folder = "C:\\Users\\Administrator\\Desktop\\workspace\\sap2000\\models"  # 必须修改为你的目标目录绝对路径！
safe_clean_files(target_folder, ['.sdb', '.py', '.txt'])