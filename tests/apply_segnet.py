# Process a image use Segnet

from segnet_utils import *
import argparse
import time
import cv2
import numpy as np
import math
import imutils
from PIL import Image

class path_detection:
    def __init__(self, model):
        self.model= model
        t1 = time.time()
        #net = jetson.inference.segNet(argv=[input.jpg, "output.jpg", "--model=fcn_resnet18.onnx", "--labels=classes.txt", "--colors=colors.txt","--input-blob=input_0", "--output_blob=output_0", ])
        self.net = jetson.inference.segNet(argv=["--model={}".format(self.model), 
                                                 "--labels=ai_model/classes.txt", 
                                                 "--colors=ai_model/colors.txt",
                                                 "--input-blob=input_0", 
                                                 "--output_blob=output_0"])
        t2 = time.time()
        print("process:",t2 - t1)

    def process(self,input_img, output_img= 'output.jpg'):
        t1 = time.time()

        # uncomment below if you need to rescale your input image
        # im = Image.open(input_img)
        # im_resized = im.resize((848,480), Image.ANTIALIAS)
        # im_resized.save(output_img)
        #print("rescale time:", time.time() - t1)
        
        # original input value on the Hello AI World example:
        # Namespace(alpha=150.0, filter_mode='linear', ignore_class='void', input_URI=input_img, network='fcn-resnet18-voc', output_URI='output.jpg', stats=False, visualize='overlay,mask')
        
        opt = argparse.Namespace()
        opt.alpha = 220
        opt.filter_mode= 'linear'
        opt.ignore_class='void'
        opt.input_URI=input_img
        opt.network='fcn-resnet18-voc'
        opt.output_URI=input_img
        opt.stats=False
        opt.visualize='overlay'
        # set the alpha blending value
        self.net.SetOverlayAlpha(opt.alpha)
        # create buffer manager
        buffers = segmentationBuffers(self.net, opt)
        sys_argv = ['segnet.py', 
                    "--model={}".format(self.model), 
                    '--labels=ai_model/classes.txt', 
                    '--colors=ai_model/colors.txt', 
                    '--input-blob=input_0', 
                    '--output_blob=output_0', 
                    input_img, 
                    output_img]
        # create video sources & outputs
        input = jetson.utils.videoSource(input_img,sys_argv)
        output = jetson.utils.videoOutput(output_img,sys_argv)
        #opt.filter_mode
        #FILTER_POINT : Nearest point sampling.
        #FILTER_LINEAR : Bilinear filtering.
        img_input = input.Capture()
        # allocate buffers for this size image
        buffers.Alloc(img_input.shape, img_input.format)
        # process the segmentation network
        self.net.Process(img_input,ignore_class='void')
        # generate the overlay
        if buffers.overlay:
            self.net.Overlay(buffers.overlay, filter_mode=opt.filter_mode)
        # # generate the mask
        #if buffers.mask:
            #self.net.Mask(buffers.mask, filter_mode=opt.filter_mode)
        # # composite the images
        #if buffers.composite:
            #jetson.utils.cudaOverlay(buffers.overlay, buffers.composite, 0, 0)
            #jetson.utils.cudaOverlay(buffers.mask, buffers.composite, buffers.overlay.width, 0)
        output.Render(buffers.output)
        print("finish mask time:",time.time()-t1)

t1 = time.time()
# pre-load detection modle, it is takes around 20s when you load it first time and 10s after first load
path_detect= segnet.path_detection("ai_model/fcn_resnet18.onnx")
print("load time used: ", time.time() - t1)

t2 = time.time()
# put a image to the detect
path_detect.process("image.jpg")
print("process time used: ", time.time() - t2)

t3 = time.time()
# also you can used it multiple times
for i in range(0,10):
  path_detect.process("image.jpg")
print("mult process time: ", time.time() - t3)
