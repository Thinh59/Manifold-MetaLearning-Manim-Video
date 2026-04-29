# Manifold Meta-Learning Presentation

Đồ án môn Nhập môn học máy. Project sử dụng thư viện Manim để tạo video giải thích về Manifold Meta-Learning theo phong cách 3Blue1Brown.

## Thông tin nhóm
- **Tên nhóm:** Ninepls
- **Môn học:** Nhập môn học máy

**Thành viên:**
1. 23122015 Nguyễn Gia Bảo
2. 23122018 Lại Nguyễn Hồng Thanh
3. 23122019 Phan Huỳnh Châu Thịnh

## Cấu trúc thư mục
- `src_video/manifold_3b1b_style_1.py`: Chứa code Manim tạo các animation (video).
- `src_video/generate_audio_1.py`: Script dùng Edge-TTS để tạo giọng đọc tự động theo kịch bản.
- `src_video/merge_video_v2_1.py`: Script ghép audio và video lại với nhau để tạo thành video hoàn chỉnh.

## Hướng dẫn chạy code
Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

Sau đó chạy lần lượt các script:
1. **Tạo Video (Manim):** `manim -pql src_video/manifold_3b1b_style_1.py ManifoldMetaLearningFlow`
2. **Tạo Audio (TTS):** `python src_video/generate_audio_1.py`
3. **Ghép Video & Audio:** `python src_video/merge_video_v2_1.py`
