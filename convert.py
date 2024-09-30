import cv2
import os

# PASCAL VOC 형식에서 YOLO 형식으로 변환하는 함수
def voc_to_yolo(x_min, y_min, x_max, y_max, img_width, img_height):
    # 중심 좌표 계산
    x_center = (x_min + x_max) / 2.0
    y_center = (y_min + y_max) / 2.0
    
    # 너비 및 높이 계산
    width = x_max - x_min
    height = y_max - y_min
    
    # 이미지 크기에 대한 상대값으로 변환
    x_center /= img_width
    y_center /= img_height
    width /= img_width
    height /= img_height
    
    return x_center, y_center, width, height

# Pascal VOC 형식을 변환하는 함수
def convert_voc_to_yolo(txt_file_path, image_dir, output_file_path):
    with open(txt_file_path, "r") as file:
        lines = file.readlines()

    # YOLO 형식으로 변환된 데이터를 저장할 파일 열기``
    with open(output_file_path, "w") as output_file:
        for line in lines:
            # 각 줄에서 정보 추출
            image_name, x_min, y_min, x_max, y_max, class_id = line.strip().split()
            
            # 이미지 파일 경로 생성
            img_path = os.path.join(image_dir, image_name)
            
            # 이미지 크기 읽기 (OpenCV 사용)
            img = cv2.imread(img_path)
            img_height, img_width, _ = img.shape
            
            # PASCAL VOC 형식에서 YOLO 형식으로 변환
            x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
            x_center, y_center, width, height = voc_to_yolo(x_min, y_min, x_max, y_max, img_width, img_height)
            
            # YOLO 형식: class_id x_center y_center width height
            output_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

# 경로 설정 (txt 파일 경로, 이미지 디렉토리 경로, 결과를 저장할 파일 경로)
txt_file_path = "path/to/your/annotations.txt"  # PASCAL VOC 형식이 적힌 txt 파일 경로
image_dir = "path/to/your/images"               # 원본 이미지가 있는 디렉토리
output_file_path = "path/to/save/yolo_annotations.txt"  # YOLO 형식으로 변환된 결과 파일 경로

# 변환 실행
convert_voc_to_yolo(txt_file_path, image_dir, output_file_path)
