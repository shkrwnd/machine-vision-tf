

from collections import deque
import cv2
from PIL import Image, ImageTk
import time
import Tkinter as tk
from tkFileDialog   import askopenfilename
import threading
from queuelib import FifoDiskQueue
import os.path
import re
import sys
import tarfile
from mygui import *
from  mytf import *
import numpy as np
from six.moves import urllib
import tensorflow as tf

tf.app.flags.DEFINE_string('image_path', '/home/ps/Documents/gui',
                           """Absolute path to image file.""")
start_time = time.time()
q = FifoDiskQueue("queuefile")
file_no = 0

def addmodel():
    a = askopenfilename()
    print a

def run_inference_on_image(image):
  #create_graph()

  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()

  create_graph()
  img  = image
  with tf.Session() as sess:

    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    counter = 2
    while 1:
	if not tf.gfile.Exists(img):
    		tf.logging.fatal('File does not exist %s', img)
  	image_data = tf.gfile.FastGFile(img, 'rb').read()
	predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
    	predictions = np.squeeze(predictions)


    	node_lookup = NodeLookup()

    	top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
    	for node_id in top_k:
      		human_string = node_lookup.id_to_string(node_id)
      		score = predictions[node_id]
      		print('%s (score = %.5f)' % (human_string, score))
	time.sleep(1.5)
	
    	img = "img/cap{0}.jpg".format(counter)
    	counter = counter + 1
	#print counter
	print ("fetching : " + img)
	time.sleep(1)





  
def run_classifier():
   image = '/home/ps/Documents/gui/img/cap1.jpg'
   run_inference_on_image(image)
   

class queuing_thread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        run_classifier()
        print "Exiting " + self.name

class camera_thread (threading.Thread):
    def __init__(self,threadID,name,counter):
	threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
	self.counter = counter
    def run(self):
	print "Starting " + self.name
        root.after(0, func=lambda: update_all(root, image_label, cam, data_label=None))
	




def saveimage(img):
    global file_no
    file_no=file_no+1
    str = "img/cap{0}.jpg".format(file_no)
    print ("Saving : " + str)
    cv2.imwrite(str,img[1])
    #cv2.imwrite('img'+f+'.jpg',img)
    ##f=f+1

def update_image(image_label, cam):
    (readsuccessful, gray_im) = cam.read()

    #print gray_im.shape
    #root.after(3,func=lambda: saveimg(gray_im))

    a = Image.fromarray(gray_im)
    b = ImageTk.PhotoImage(image=a)
    image_label.configure(image=b)
    image_label._image_cache = b  # avoid garbage collection
    root.update()


def update_fps(fps_label):
    frame_times = fps_label._frame_times
    frame_times.rotate()
    frame_times[0] = time.time()
    sum_of_deltas = frame_times[0] - frame_times[-1]
    count_of_deltas = len(frame_times) - 1
    try:
        fps = int(float(count_of_deltas) / sum_of_deltas)
    except ZeroDivisionError:
        fps = 0
    fps_label.configure(text='FPS: {}'.format(fps))


def update_all(root, image_label, cam, data_label):
    update_image(image_label, cam)
    
    interval = time.time() - start_time
    #print interval
    if(interval >2 ):
	
	saveimage(cam.read())
        global q
 	q = FifoDiskQueue("queuefile")
	#q.push(b
	global start_time 
        start_time = time.time()

    #update_fps(fps_label)
    root.after(2, func=lambda: update_all(root, image_label, cam,data_label))

def dir():
   pass


def capturef():
    pass


def create_menu(root):
    menu = tk.Menu(root)
    root.config(menu=menu)
    # menu 1
    filemenu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New")
    filemenu.add_command(label="Open...", command=addmodel)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    # menu 2

    cammenu = tk.Menu(menu)
    menu.add_cascade(label="Camera",menu=cammenu)
    cammenu.add_command(label="Start Camera")
    cammenu.add_command(label="Stop Camera")
    cammenu.add_separator()
    cammenu.add_command(label="Capture Image",command=capturef)

   
if __name__ == '__main__':
    
    root = tk.Tk() 
    #m1 = tk.PanedWindow()
    #m1.pack(fill=BOTH,expand = 1)
    create_menu(root)
    pane_left = tk.PanedWindow(root)
    pane_left.pack()
    image_label = tk.Label(master=pane_left)    # label for the video frame
    image_label.pack()
    pane_left.add(image_label)

    pane_right = tk.PanedWindow(pane_left)
    #pane_right.pack()
    pane_left.add(pane_right)

    data_label = tk.Label(master=pane_right,text = "Classifiers")
    data_label.pack()
    pane_right.add(data_label)
    
    
    
    cam = cv2.VideoCapture(0) 
    #fps_label = tk.Label(master=root).grid(row=0,column=1)# label for fps
    #fps_label._frame_times = deque([0]*5)  # arbitrary 5 frame average FPS
    #fps_label.pack()
    # quit button
    quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root))

    thread1 = camera_thread(1,"camera-thread",1)
    thread1.run()
    thread2 = queuing_thread(2,"queue-thread",2)
    thread2.start()
    #quit_button.pack()
    # setup the update callback
    #root.after(0, func=lambda: update_all(root, image_label, cam, fps_label=None))
    
    root.mainloop()
#
