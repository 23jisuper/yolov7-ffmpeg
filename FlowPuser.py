import subprocess


##########################    定义推流器      ###################################

class StreamPusher:
    def __init__(self, rtmp_url):       #接受一个参数rtmq_url 该参数受用于指定rtmq服务器地址的字符串
        # 创建FFmpeg命令行参数
        ffmpeg_cmd = ['ffmpeg',
                      '-y',  # 覆盖已存在的文件
                      '-f', 'rawvideo',  #指定输入格式为原始视频帧数据
                      '-pixel_format', 'bgr24',    #指定输入数据的像素格式为BGR24(一种图像颜色编码格式)
                      '-video_size', '640x480',    #指定输入视频的尺寸为640*480
                      '-i', '-',  # 从标准输入读取数据
                      '-c:v', 'libx264',      #指定视频编码器为libx264(H.264编码器)
                      '-preset', 'ultrafast',   #使用ultrafast预设，以获得更快的编码速度
                      '-tune', 'zerolatency', #使用zerolatency调整 以降低延迟
                      '-pix_fmt', 'yuv420p',     #指定输出视频像素格式为yuv420p
                      '-f', 'flv',      #指定输出格式为FLV
                      rtmp_url]   #指定输出目标为‘rtmp_url' 即RTMP服务器地址
        print('ffmpeg_cmd:', ffmpeg_cmd)
        # 启动 ffmpeg
        self.ffmepg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    def streamPush(self, frame):    #用于推送视频帧数据到FFmpeg进程
        self.ffmepg_process.stdin.write(frame.tobytes())
