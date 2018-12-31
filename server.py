import argparse
import asyncio
import json
import logging
import math
import os
import time
import wave

import cv2
import numpy
from aiohttp import web

import sys
import traceback
import tellopy
import av

from aiortc import RTCPeerConnection, RTCSessionDescription
from aiortc.mediastreams import (AudioFrame, AudioStreamTrack, VideoFrame,
                                 VideoStreamTrack)

ROOT = os.path.dirname(__file__)


def frame_from_bgr(data_bgr):
    data_yuv = cv2.cvtColor(data_bgr, cv2.COLOR_BGR2YUV_YV12)
    return VideoFrame(width=data_bgr.shape[1], height=data_bgr.shape[0], data=data_yuv.tobytes())


def frame_from_gray(data_gray):
    data_bgr = cv2.cvtColor(data_gray, cv2.COLOR_GRAY2BGR)
    data_yuv = cv2.cvtColor(data_bgr, cv2.COLOR_BGR2YUV_YV12)
    return VideoFrame(width=data_bgr.shape[1], height=data_bgr.shape[0], data=data_yuv.tobytes())


def frame_to_bgr(frame):
    data_flat = numpy.frombuffer(frame.data, numpy.uint8)
    data_yuv = data_flat.reshape(
        (math.ceil(frame.height * 12 / 8), frame.width))
    return cv2.cvtColor(data_yuv, cv2.COLOR_YUV2BGR_YV12)


class VideoTransformTrack(VideoStreamTrack):
    def __init__(self, container, video_stream, width, height):
        self.container = container
        self.video_stream = video_stream
        self.frame_skip = 300
        self.total_frame = 0
        self.frame = VideoFrame(width=width, height=height)

    async def recv(self):
        for packet in self.container.demux(self.video_stream):
            try:
                frames = packet.decode()
                self.total_frame = self.total_frame + len(frames)
                for frm in frames:
                    if 0 < self.frame_skip:
                        self.frame_skip = self.frame_skip - 1
                        continue
                    start_time = time.time()
                    self.frame = frame_from_bgr(numpy.array(frm.to_image()))
                    self.frame_skip = 1
                    #self.frame_skip = int((time.time() - start_time)/frm.time_base)
                    cv2.waitKey(1)
                    return self.frame
            except AVError as err:
                print(err)
                return self.frame

        return self.frame


async def index(request):
    content = open(os.path.join(ROOT, 'index.html'), 'r').read()
    return web.Response(content_type='text/html', text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, 'client.js'), 'r').read()
    return web.Response(content_type='application/javascript', text=content)


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(
        sdp=params['sdp'],
        type=params['type'])

    pc = RTCPeerConnection()
    pc._consumers = []
    pcs.append(pc)

    width = 1920
    height = 1080
    local_video = VideoTransformTrack(
        container=container, video_stream=video_stream, width=width, height=height)
    pc.addTrack(local_video)

    @pc.on('datachannel')
    def on_datachannel(channel):
        @channel.on('message')
        def on_message(message):
            if message == "connect":
                vs.queue = []  # キューイングされているデータをクリア
            elif message == "ping":
                channel.send('pong')
            elif message == "takeoff":
                drone.takeoff()
            elif message == "down":
                drone.down(50)
            elif message == "land":
                drone.land()

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type='application/json',
        text=json.dumps({
            'sdp': pc.localDescription.sdp,
            'type': pc.localDescription.type
        }))


pcs = []
drone = {}
container = {}
video_stream = {}
vs = {}


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='WebRTC audio / video / data-channels demo')
    parser.add_argument('--port', type=int, default=8080,
                        help='Port for HTTP server (default: 8080)')
    parser.add_argument('--verbose', '-v', action='count')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    drone = tellopy.Tello()
    drone.connect()
    drone.wait_for_connection(60.0)
    drone.start_video()
    vs = drone.get_video_stream()
    container = av.open(vs)
    video_stream = next(s for s in container.streams if s.type == 'video')

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_get('/', index)
    app.router.add_get('/client.js', javascript)
    app.router.add_post('/offer', offer)
    web.run_app(app, port=args.port)
