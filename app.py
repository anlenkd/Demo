import os
import subprocess
import streamlit as st
from PIL import Image

# 修改为您的权重文件路径和YOLOv5检测脚本路径
WEIGHTS_PATH = r"D:\YoLoV5_run\project\best.pt"
DETECT_SCRIPT_PATH = r"D:\YoLoV5_run\yolov5\detect.py"
RESULT_FOLDER = r'static/results'

# 创建结果文件夹
os.makedirs(RESULT_FOLDER, exist_ok=True)


def run_detection(weights_path, input_image_path):
    # 构建目标检测命令
    command = f'python "{DETECT_SCRIPT_PATH}" --weights "{weights_path}" --source "{input_image_path}" --img 640 --conf 0.25'
    command += f' --project "{RESULT_FOLDER}" --name "result" --exist-ok'  # 确保不会覆盖

    # 执行命令
    subprocess.run(command, shell=True)


def load_and_display_image(image_path):
    # 打开和显示图像
    image = Image.open(image_path)
    st.image(image, caption='预测结果', use_column_width=True)


def delete_generated_images():
    # 删除生成的结果图像
    results_dir = os.path.join(RESULT_FOLDER, "result")
    # 遍历并删除所有结果图像
    for img in os.listdir(results_dir):
        img_path = os.path.join(results_dir, img)
        if img.endswith(('.jpg', '.png')):
            os.remove(img_path)
            print(f"Deleted: {img_path}")


def main():
    st.title("目标检测应用")
    st.write("请上传您想要进行目标检测的图片。")

    # 图片上传组件
    uploaded_file = st.file_uploader("选择图片...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # 将上传的文件保存到临时文件
        input_image_path = os.path.join(RESULT_FOLDER, uploaded_file.name)
        with open(input_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption='上传的图片', use_column_width=True)

        # 运行检测模型
        st.write("正在进行目标检测，请稍候...")
        run_detection(WEIGHTS_PATH, input_image_path)

        # 查找生成的结果图像
        result_images = [img for img in os.listdir(os.path.join(RESULT_FOLDER, "result")) if
                         img.endswith(('.jpg', '.png'))]

        # 找到最新生成的结果图像
        if result_images:
            latest_image = sorted(result_images)[-1]
            result_image_path = os.path