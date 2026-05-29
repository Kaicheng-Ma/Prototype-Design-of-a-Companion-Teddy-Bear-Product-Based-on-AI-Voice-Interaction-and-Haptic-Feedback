import pyaudio
import numpy as np
import time
import wave
import os

# 基本参数设置
CHUNK = 1024             # 每个音频块的采样点数
RATE = 44100             # 采样率（Hz）
FORMAT = pyaudio.paInt16 # 采样格式
CHANNELS = 1             # 声道数（单声道）

def list_input_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"输入设备 ID {i} - {device_info.get('name')}")
    p.terminate()

def calibrate_noise(stream, duration=20.0, factor=1.5):
    """
    环境噪音校准：录制一段时间的环境噪音，
    计算每块音频的 FFT 能量均值，再取平均值，
    并将阈值设定为：平均能量 * factor
    """
    print("开始环境噪声校准，请保持安静...")
    num_frames = int(RATE / CHUNK * duration)
    energies = []
    for i in range(num_frames):
        # 读取一块音频数据，避免溢出异常
        data = stream.read(CHUNK, exception_on_overflow=False)
        # 将字节数据转换为 numpy 数组
        frame = np.frombuffer(data, dtype=np.int16)
        # 对音频数据进行 FFT
        fft = np.fft.rfft(frame)
        magnitude = np.abs(fft)
        # 计算均值作为能量值
        energy = np.mean(magnitude)
        energies.append(energy)
        print(f"第 {i+1} 次能量值: {energy:.2f}")  # 打印每次读取的能量值
    avg_energy = np.mean(energies)
    threshold = avg_energy * factor
    print(f"环境噪声平均能量: {avg_energy:.2f}，阈值设置为: {threshold:.2f}")
    return threshold

def record_voice_command(stream, duration=3.0, p=None, output_filename="command.wav"):
    """
    录制语音命令并保存为 WAV 文件
    """
    print("开始录音...")
    frames = []
    num_frames = int(RATE / CHUNK * duration)
    for i in range(num_frames):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
    # 保存录音到 WAV 文件
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"录音保存到 {output_filename}")

def main():
    # 列出所有输入设备
    list_input_devices()
    
    # 初始化 PyAudio
    p = pyaudio.PyAudio()
    # 选择特定的输入设备 ID（根据列出的设备选择合适的 ID）
    input_device_id = int(input("请输入要使用的输入设备 ID: "))
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=input_device_id,
                    frames_per_buffer=CHUNK)
    
    # 先校准环境噪音，计算阈值
    threshold = calibrate_noise(stream, duration=20.0, factor=1.5)
    
    print("开始监听语音命令，当检测到能量超过阈值时，将启动录音...")
    
    last_print_time = time.time()
    
    flag=True

    try:
        while flag:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frame = np.frombuffer(data, dtype=np.int16)
            fft = np.fft.rfft(frame)
            magnitude = np.abs(fft)
            energy = np.mean(magnitude)
            
            # 每隔五秒打印一次能量值
            current_time = time.time()
            if current_time - last_print_time >= 5:
                print(f"当前能量: {energy:.2f}")
                last_print_time = current_time
            
            if energy > threshold:
                flag=False
                print(f"检测到语音输入 (能量: {energy:.2f} > 阈值: {threshold:.2f})")
                # 修改保存路径
                output_dir = r'C:\Users\18660\Desktop\00dkuclass\info104\000final'
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                output_filename = os.path.join(output_dir, "command.wav")
                record_voice_command(stream, duration=8.0, p=p, output_filename=output_filename)
                # 录音后等待 10 秒，避免连续触发
                time.sleep(10.0)
            else:
                # 小睡眠降低 CPU 占用
                time.sleep(0.01)
    except KeyboardInterrupt:
        print("退出监听...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()