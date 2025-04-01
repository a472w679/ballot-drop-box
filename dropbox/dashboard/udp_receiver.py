import base64
import os
import socket
import struct
import threading
from collections import deque
from datetime import datetime
from io import BytesIO

import cv2
import numpy as np
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class UDPVideoReceiver:
    def __init__(self):
        self.udp_ip = "0.0.0.0"
        self.udp_port = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        self.channel_layer = get_channel_layer()
        self.video_fps = 30
        self.prologue_frames_buffer = deque([], maxlen=2*self.video_fps)  # stores frames before motion happens continuously 
        self.max_content_frames = 5*self.video_fps
        self.content_frames_buffer = []
        self.motion_detected_state = False  # informs whehter or not frames should be stored in buffer 
        self.start_time = datetime.now()  # the time is starts recording (default on __init__) 
        self.video_directory = os.path.join(os.path.dirname(__file__), "static", "media") 

    def start_receiving(self):
        print(f"UDP receiver started on port {self.udp_port}")
        MIN_PACKET_SIZE = 12 
        while True:
            data, addr = self.sock.recvfrom(65536)  # Max UDP packet size

            # Check if packet is too small
            if len(data) < MIN_PACKET_SIZE:
                continue 

            
            # Verify that there enough data for the claimed JPEG size
            try:
                sender_id = struct.unpack('!I', data[:4])[0]
                jpeg_size = struct.unpack('!I', data[4:8])[0]
                motion_detected = struct.unpack('?', data[8:9])[0]
            except struct.error:
                continue 
                
            # Check if jpeg_size is reasonable
            if jpeg_size > 10 * 1024 * 1024:  # 10MB max
                continue 
                
            # Verify complete JPEG data was received
            if len(data) < 9 + jpeg_size:
                continue 
                
            # Extract and validate JPEG data
            jpeg_bytes = data[9:9+jpeg_size]
            
            # Verify JPEG header
            if len(jpeg_bytes) < 2 or jpeg_bytes[0] != 0xFF or jpeg_bytes[1] != 0xD8:
                continue 

            # encode jpg data to b64 
            jpg_base64 = base64.b64encode(jpeg_bytes).decode('utf-8')
            
            # Broadcast to WebSocket clients
            async_to_sync(self.channel_layer.group_send)(
                "video_group",
                {
                    "type": "video.frame",
                    "frame": jpg_base64,
                    "sender_id": sender_id
                }
            )

            # save a video recording if motion is detected 
            self.save_video_recording(motion_detected, jpeg_bytes)




    def jpeg_to_frame(self, jpeg_bytes):
        """
        Convert JPEG bytes to OpenCV frame

        Args: 
            jpeg_bytes (bytes): jpeg frames in bytes 

        Returns: 
            cv2.typing.MatLike
        """
        try:
            np_array = np.frombuffer(jpeg_bytes, dtype=np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            return frame
        except Exception as e:
            print(f"Error decoding JPEG: {e}")
            return None


    def save_buffer_as_video(self, frame_buffer, fps):
        """
        Save buffered frames as video file

        Args: 
            frame_buffer (cv2.typing.MatLike): frames taken from live feed
            fps (float): the real number of frames per time taken since motion was detected  

        Returns: 
            str of video  
        """
        if not frame_buffer:
            return None


        height, width = frame_buffer[0].shape[:2]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(self.video_directory, f"video_{timestamp}.mp4")
        
        # Create VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        # content 
        for frame in frame_buffer:
            out.write(frame)
        
        print(timestamp, ": Motion Detected, Saved Video with FPS(", fps, ")")
        out.release()
        
        return output_path

    def save_video_recording(self, motion_detected, jpeg_bytes): 
        '''
        Saves past 10-15 seconds of live feed to disk if motion is detected  

        Args: 
            motion_detected (bool): 
            jpeg_bytes ()
        '''
        frame = self.jpeg_to_frame(jpeg_bytes)
        self.prologue_frames_buffer.append(frame)
        if motion_detected and not self.motion_detected_state: 
            print("DEBUG: motion detected, recording in progress")
            self.motion_detected_state = True 

            # save prologue frames 
            if self.prologue_frames_buffer: 
                for frame in list(self.prologue_frames_buffer): 
                    self.content_frames_buffer.append(frame)
            self.start_time = datetime.now() # set recording start 

        # Save the video if motion is detected  
        if self.motion_detected_state: 
            # Convert JPEG bytes to OpenCV frame
            if frame is not None:
                num_frames = len(self.content_frames_buffer)
                if num_frames != (self.max_content_frames + self.prologue_frames_buffer.maxlen): 
                    self.content_frames_buffer.append(frame)
                else:  # save video 
                    seconds = datetime.now() - self.start_time 
                    realfps = num_frames / seconds.total_seconds()   # frames per second 
                    # print(num_frames, seconds.total_seconds(), realfps)
                    save_buffer_as_video_thread = threading.Thread(target=self.save_buffer_as_video, daemon=True, args=(self.content_frames_buffer.copy(), realfps,))
                    save_buffer_as_video_thread.start()

                    self.motion_detected_state = False 
                    self.content_frames_buffer.clear()
                    self.prologue_frames_buffer.clear()




# To start in Django
def start_udp_receiver():
    receiver = UDPVideoReceiver()
    receiver.start_receiving()


