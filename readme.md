# Getting Tello Video using WebRTC

## Requirements

1. [Python 3.6](https://www.python.org/downloads/release/python-368/) -- includes PIP, etc
2. [Microsoft Build Tools for Visual Studio 2017](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017) -- only need "Windows 10 SDK"
3. [VS Code](https://code.visualstudio.com/download)
4. Python Extension Pack for VS Code (donjayamanne.python-extension-pack) -- installs other VS Code extensions
5. FFmpeg -- see PyAV below

## Using This Code

1. enter `pip install -r requirements.txt`
2. turn on the Tello drone
3. connect to drone via WiFi
4. enter `python server.py`
5. in Chrome go to http://localhost:8080
6. click the Start button
7. signaling begins (may need to wait for a bit)
8. when WebRTC connection is established, the video displays in the browser

## References

* [Some Japanese developer figured out how to get video working with WebRTC](https://qiita.com/a-baba/items/d728d580f89473c5fd18)
* [Audio, video and data channel server](https://github.com/jlaine/aiortc/tree/master/examples/server)
* [Fix Python error "Visual C++ is required"](https://www.scivision.co/python-windows-visual-c++-14-required/)
* [Error installing module av](https://github.com/hanyazou/TelloPy/issues/12)
* [PyAV](https://github.com/mikeboers/PyAV)
* [PyAV Installation](https://github.com/mikeboers/PyAV/blob/develop/docs/installation.rst)
* [Installing PyAV under Windows without Conda](https://github.com/mikeboers/PyAV/issues/199#issuecomment-287540308)

## Installing PyAV under Windows

1. download FFmpeg ([shared and dev packages](https://ffmpeg.zeranoe.com/builds/))
2. unpack them somewhere (like C:\ffmpeg)
3. add paths for compiler:
```
export INCLUDE="$INCLUDE;c:/ffmpeg/include"
export LIB="$LIB;c:/ffmpeg/lib"
export PATH="$PATH;c:/ffmpeg/bin"
```
4. install PyAV: `pip install av==0.4.1` (as per requirements.txt)
5. continue with installing requirements (above)
