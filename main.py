import argparse
import time

import cv2
import imutils
from FlowPuser import StreamPusher
from Yolov7Compents import YOLOv7



rtmp_server = 'rtmp://10.16.89.73:1935/video'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, default='video/test.mp4', help="image path")
    parser.add_argument('--modelpath', type=str, default='models/yolov7-tiny_384x640.onnx',
                        choices=["models/yolov7_640x640.onnx", "models/yolov7-tiny_640x640.onnx",
                                 "models/yolov7_736x1280.onnx", "models/yolov7-tiny_384x640.onnx",
                                 "models/yolov7_480x640.onnx", "models/yolov7_384x640.onnx",
                                 "models/yolov7-tiny_256x480.onnx", "models/yolov7-tiny_256x320.onnx",
                                 "models/yolov7_256x320.onnx", "models/yolov7-tiny_256x640.onnx",
                                 "models/yolov7_256x640.onnx", "models/yolov7-tiny_480x640.onnx",
                                 "models/yolov7-tiny_736x1280.onnx", "models/yolov7_256x480.onnx"],
                        help="onnx filepath")
    parser.add_argument('--confThreshold', default=0.3, type=float, help='class confidence')
    parser.add_argument('--nmsThreshold', default=0.5, type=float, help='nms iou thresh')
    args = parser.parse_args()

    # Initialize YOLOv7 object detector
    yolov7_detector = YOLOv7(args.modelpath, conf_thres=args.confThreshold, iou_thres=args.nmsThreshold)

    VID_FORMATS = ['asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'wmv']  # include video suffixes
    imgpath = args.imgpath
    print(imgpath.split('.')[-1])
    if imgpath.split('.')[-1] in VID_FORMATS:
        cap = cv2.VideoCapture(0)
        pusher = StreamPusher(rtmp_server)
        while True:
            success, srcimg = cap.read()
            srcimg = imutils.resize(srcimg, width=640)
            t1 = time.time()
            boxes, scores, class_ids = yolov7_detector.detect(srcimg)
            print(time.time() - t1)  # 测量处理一帧图像的时间 用于评估模型的处理速度或性能(推理时间)
            # Draw detections
            dstimg = yolov7_detector.draw_detections(srcimg, boxes, scores, class_ids)
            print(time.time() - t1)  # 测量了模型的推理时间以及绘制检测结果的时间
            winName = 'Deep learning object detection in OpenCV'
            # cv2.namedWindow(winName, 0)
            # cv2.imshow(winName, dstimg)

            cv2.waitKey(1)
            pusher.streamPush(dstimg)
        cv2.destroyAllWindows()
    else:
        srcimg = cv2.imread(args.imgpath)
        # Detect Objects
        t1 = time.time()
        boxes, scores, class_ids = yolov7_detector.detect(srcimg)
        print(time.time() - t1)
        # Draw detections
        dstimg = yolov7_detector.draw_detections(srcimg, boxes, scores, class_ids)
        print(time.time() - t1)
        winName = 'Deep learning object detection in OpenCV'
        cv2.namedWindow(winName, 0)
        cv2.imshow(winName, dstimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()