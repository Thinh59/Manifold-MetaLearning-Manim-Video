"""
Cách chạy: python src_video/merge_video_v2_1.py
"""
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import os


audio_files = [
    "audio/s01_intro.mp3",
    "audio/s02_meta_learning.mp3",
    "audio/s03_maml.mp3",
    "audio/s04_blackbox_limits.mp3",
    "audio/s05_physics.mp3",
    "audio/s06_leo.mp3",
    "audio/s07_manifold_idea.mp3",
    "audio/s08_lifting.mp3",
    "audio/s09_loss.mp3",
    "audio/s10_distribution.mp3",
    "audio/s11_model_f.mp3",
    "audio/s12_results.mp3",
    "audio/s13_hybrid.mp3",
    "audio/s14_conclusion.mp3",
]

video_path = "media/videos/manifold_3b1b_style_1/1080p60/ManifoldMetaLearningFlow.mp4"

output_path = "manifold_meta_learning_v2.mp4"


def load_audio_clips(file_list):
    clips = []
    missing = []
    print("\n📋 Kiểm tra file audio:")
    for f in file_list:
        if os.path.exists(f):
            clip = AudioFileClip(f)
            print(f"   ✅ {f:45s} ({clip.duration:.1f}s)")
            clips.append(clip)
        else:
            print(f"   ❌ THIẾU: {f}")
            missing.append(f)
    return clips, missing


def main():
    if not os.path.exists(video_path):
        print(f"\n❌ LỖI: Không tìm thấy video tại:\n   {video_path}")
        print("\n👉 Hãy render Manim trước:")
        print("   manim -pqh manifold_3b1b_style_1.py ManifoldMetaLearningFlow")
        return

    clips, missing = load_audio_clips(audio_files)

    if not clips:
        print("\n❌ LỖI: Không có audio nào để ghép!")
        return

    if missing:
        print(f"\n⚠️  Thiếu {len(missing)} file audio. Tiếp tục với {len(clips)} file có sẵn...")

    print("\n🔗 Đang ghép audio...")
    final_audio = concatenate_audioclips(clips)
    audio_duration = final_audio.duration
    print(f"   Tổng thời lượng audio : {audio_duration:.1f}s  ({audio_duration/60:.1f} phút)")

    print("\n🎬 Đang tải video...")
    video_clip = VideoFileClip(video_path)
    video_duration = video_clip.duration
    print(f"   Thời lượng video      : {video_duration:.1f}s  ({video_duration/60:.1f} phút)")

    diff = audio_duration - video_duration
    if diff > 0:
        print(f"   ℹ️  Audio dài hơn video {diff:.1f}s → kéo dài khung cuối video")
        video_clip = video_clip.set_duration(audio_duration)
    elif diff < 0:
        print(f"   ℹ️  Video dài hơn audio {abs(diff):.1f}s → cắt ngắn video")
        video_clip = video_clip.subclip(0, audio_duration)
    else:
        print("   ✅ Audio và video khớp thời lượng")

    final_video = video_clip.set_audio(final_audio)
    print(f"\n📤 Đang xuất → {output_path}")
    final_video.write_videofile(
        output_path,
        fps=60,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast",
        logger="bar",
    )
    print(f"\n✅ THÀNH CÔNG! Video đã lưu tại: {output_path}")

    final_audio.close()
    video_clip.close()
    final_video.close()


if __name__ == "__main__":
    main()
