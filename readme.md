# Getting Tello Video using WebRTC

## Requirements

1. [Python 3.6](https://www.python.org/downloads/release/python-368/) -- includes PIP, etc
1. [Microsoft Build Tools for Visual Studio 2017](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017) -- only need "Windows 10 SDK"
1. [VS Code](https://code.visualstudio.com/download)
1. Python Extension Pack for VS Code (donjayamanne.python-extension-pack) -- installs other VS Code extensions

## Using This Code

1. enter `pip install -r requirements.txt` (or `pip install aiohttp aiortc opencv-python`)
1. turn on the Tello drone
1. connect to drone via WiFi
1. enter `python server.py`
1. in Chrome go to http://localhost:8080
1. click the Start button
1. signaling begins (may need to wait for a bit)
1. when WebRTC connection is established, the video displays in the browser

## References

* [Some Japanese developer figured out how to get video working with WebRTC](https://qiita.com/a-baba/items/d728d580f89473c5fd18)
* [Audio, video and data channel server](https://github.com/jlaine/aiortc/tree/master/examples/server)
* [Fix Python error "Visual C++ is required"](https://www.scivision.co/python-windows-visual-c++-14-required/)
