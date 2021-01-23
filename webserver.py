import gc
import machine
import json
import time
import camera


from microWebSrv import MicroWebSrv

class webcam():

    def __init__(self):
        self.framesize = camera.FRAME_VGA
        self.routeHandlers = [
            ("/", "GET", self._httpHandlerIndex),
            ("/stream/<d>", "GET", self._httpStream)
        ]

    def run(self, app_config):
        self.led = machine.Pin(app_config['led'], machine.Pin.OUT)

        # Camera resilience - if we fail to init try to deinit and init again
        camera.init(0, format=camera.JPEG, framesize=self.framesize)      #ESP32-CAM 

        mws = MicroWebSrv(routeHandlers=self.routeHandlers, webPath="www/")
        mws.Start(threaded=True)
        gc.collect()

    def _httpStream(self, httpClient, httpResponse, routeArgs):
        image = camera.capture()

        headers = { 'Last-Modified' : 'Fri, 1 Jan 2018 23:42:00 GMT', \
                    'Cache-Control' : 'no-cache, no-store, must-revalidate' }

        httpResponse.WriteResponse(code=200, headers=headers,
                                    contentType="image/jpeg",
                                    contentCharset="UTF-8",
                                    content=image)
        
    def _httpHandlerIndex(self, httpClient, httpResponse):
        f = open("www/index.html", "r")
        content =  f.read()
        f.close()

        httpResponse.WriteResponseOk(headers=None,
                                    contentType="text/html",
                                    contentCharset="UTF-8",
                                    content=content)                                

