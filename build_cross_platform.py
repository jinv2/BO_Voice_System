import subprocess
import os
import platform
import shutil

def build():
    os_type = platform.system()
    print(f"🚀 Detected OS: {os_type}")
    
    # 1. 确保在根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)
    
    # 2. 检查依赖
    print("📦 Checking dependencies...")
    subprocess.run(["pip", "install", "pyinstaller", "Pillow", "pyperclip"], check=True)
    
    # 3. 清理旧构建
    dirs_to_clean = ["build", "dist", "BO_Matrix_Dist"]
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"🧹 Cleaned existing {d} directory.")
    
    # 4. 执行 PyInstaller 构建
    # Windows: .exe, Mac: .app/binary, Linux: binary
    print(f"🏗️  Building executable for {os_type}...")
    
    add_data_sep = ";" if os_type == "Windows" else ":"
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        f"--add-data=assets{add_data_sep}assets",
        "--name=BO_Matrix",
        "src/bo_ui.py"
    ]
    
    subprocess.run(cmd, check=True)
    
    # 5. 整理分发文件夹
    dist_folder = "BO_Matrix_Dist"
    os.makedirs(dist_folder)
    
    # 移动二进制文件
    shutil.move("dist/BO_Matrix", os.path.join(dist_folder, "BO_Matrix"))
    
    # 复制文档
    docs = ["DOCS_BO_FEATURES.md", "INSTALLATION_GUIDE.md"]
    for doc in docs:
        if os.path.exists(doc):
            shutil.copy(doc, dist_folder)
            print(f"📝 Copied {doc} to distribution folder.")
            
    print(f"\n✅ Build Complete! Your {os_type} version is ready in: {os.path.abspath(dist_folder)}")

if __name__ == "__main__":
    build()
