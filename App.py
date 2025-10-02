import streamlit as st
import subprocess
import os
import tempfile
import mimetypes
import zipfile
import io

# App title
st.markdown("<h1 style='text-align: center;'>🎬 Universal Media Converter</h1>", unsafe_allow_html=True)
st.write("Easily convert any **video** or **audio** file into different formats with custom or preset FFmpeg settings.")

st.divider()

# Upload multiple files
uploaded_files = st.file_uploader("📂 Upload your files", type=None, accept_multiple_files=True)

# Format selector
formats = ["amv", "avi", "mp3", "mkv", "mov", "flv", "wmv", "wav", "aac", "ogg", "mp4"]
output_format = st.selectbox("🎯 Choose output format", formats)

# Sidebar for advanced settings
st.sidebar.header("⚙️ Conversion Settings")

# Presets
presets = {
    "Default (No Changes)": {},
    "Mobile Friendly": {"video_bitrate": "800k", "resolution": "854x480", "fps": "24", "audio_bitrate": "128k", "sample_rate": "44100", "channels": "2"},
    "High Quality": {"video_bitrate": "2500k", "resolution": "1920x1080", "fps": "30", "audio_bitrate": "320k", "sample_rate": "48000", "channels": "2"},
    "Low Size (Compressed)": {"video_bitrate": "500k", "resolution": "640x360", "fps": "20", "audio_bitrate": "96k", "sample_rate": "22050", "channels": "1"}
}

preset_choice = st.sidebar.selectbox("🎛️ Choose a preset", list(presets.keys()))

# Default values from preset
preset_values = presets[preset_choice]

video_bitrate = st.sidebar.text_input("🎥 Video Bitrate", preset_values.get("video_bitrate", ""))
resolution = st.sidebar.text_input("🖥️ Resolution", preset_values.get("resolution", ""))
fps = st.sidebar.text_input("🎞️ Frame Rate", preset_values.get("fps", ""))
audio_bitrate = st.sidebar.text_input("🎵 Audio Bitrate", preset_values.get("audio_bitrate", ""))
sample_rate = st.sidebar.text_input("🎚️ Sample Rate", preset_values.get("sample_rate", ""))
audio_channels = st.sidebar.selectbox(
    "🔊 Audio Channels",
    ["Default", "1 (Mono)", "2 (Stereo)"],
    index=0 if "channels" not in preset_values else (1 if preset_values["channels"] == "1" else 2)
)

st.divider()

if uploaded_files:
    st.subheader("📺 Preview")
    for file in uploaded_files:
        mime_type, _ = mimetypes.guess_type(file.name)
        if mime_type:
            if mime_type.startswith("video"):
                st.video(file)
            elif mime_type.startswith("audio"):
                st.audio(file)
        else:
            st.write(f"📄 {file.name} (cannot preview)")

    if st.button("🚀 Convert All Files"):
        progress_bar = st.progress(0)
        converted_files = []

        for i, uploaded_file in enumerate(uploaded_files):
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_input:
                temp_input.write(uploaded_file.read())
                temp_input.flush()
                base_name = os.path.splitext(uploaded_file.name)[0]
                output_file = os.path.join(tempfile.gettempdir(), f"{base_name}_converted.{output_format}")

            # Build FFmpeg command
            ffmpeg_cmd = ["ffmpeg", "-i", temp_input.name, "-y"]

            if video_bitrate:
                ffmpeg_cmd += ["-b:v", video_bitrate]
            if resolution:
                ffmpeg_cmd += ["-s", resolution]
            if fps:
                ffmpeg_cmd += ["-r", fps]
            if audio_bitrate:
                ffmpeg_cmd += ["-b:a", audio_bitrate]
            if sample_rate:
                ffmpeg_cmd += ["-ar", sample_rate]
            if audio_channels != "Default":
                ffmpeg_cmd += ["-ac", audio_channels.split()[0]]

            ffmpeg_cmd.append(output_file)

            # Run ffmpeg
            process = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if process.returncode == 0 and os.path.exists(output_file):
                with open(output_file, "rb") as f:
                    converted_files.append((f"{base_name}_converted.{output_format}", f.read()))
                st.success(f"✅ {uploaded_file.name} converted successfully!")
            else:
                st.error(f"❌ Failed to convert {uploaded_file.name}")
                st.text(process.stderr.decode("utf-8"))

            # Cleanup
            try:
                os.remove(temp_input.name)
                if os.path.exists(output_file):
                    os.remove(output_file)
            except:
                pass

            progress_bar.progress(int(((i + 1) / len(uploaded_files)) * 100))

        # Download section
        if converted_files:
            st.subheader("⬇️ Download Your Files")

            for file_name, file_bytes in converted_files:
                st.download_button(
                    label=f"📥 {file_name}",
                    data=file_bytes,
                    file_name=file_name,
                    mime="application/octet-stream"
                )

            # ZIP option
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                for file_name, file_bytes in converted_files:
                    zipf.writestr(file_name, file_bytes)
            zip_buffer.seek(0)

            st.download_button(
                label="📦 Download All as ZIP",
                data=zip_buffer,
                file_name="converted_files.zip",
                mime="application/zip"
            )

st.divider()
st.markdown(
    """
    💡 **Help & Support**  
    If something doesn’t work, please contact:  
    📩 **cambro4072@icloud.com**
    """,
    unsafe_allow_html=True
)
