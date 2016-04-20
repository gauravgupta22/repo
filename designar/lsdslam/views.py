from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import render
from lsdslam.models import Video
import json
from datetime import datetime
import random, string
import os
from subprocess import Popen


def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))



def index(request):
	if request.method == 'POST':
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		s=datetime.now().strftime('%Y%m%d%H%M%S')+randomword(5)
		BASE_DIR=BASE_DIR+"/media/videos/"+s
		ext="mp4"
		VIDEO_URL="/media/videos/"+s
		PLOT_URL="/media/plot/"+s
		CAMERA_URL="/media/camera/"+s

		def videoLocation(i):
			return BASE_DIR+str(i)+"."+ext

		def urlLocation(i):
			return VIDEO_URL+str(i)+"."+ext
		    
		try:
	       	    	video=request.FILES['file']
		except:
		    	return HttpResponse("error")
		
		print video.name
		ext=video.name.split(".")[-1].lower()
		video_name=s+"."+ext
		newvideo = Video(name=video_name,videofile = request.FILES['file'])
		newvideo.save()

		camera_name=s+".txt"
		plot_name=s+".png"

		p1 = Popen(['/home/gaurav/Volume3/designar/lsdslam/scripts/lsd_slam_core'])
		p2 = Popen(['/home/gaurav/Volume3/designar/lsdslam/scripts/lsd_slam_viewer',camera_name])
		p3 = Popen(['/home/gaurav/Volume3/designar/lsdslam/scripts/video_image',BASE_DIR+"."+ext,plot_name ])

		response_dict={}
        	response_dict["camera"]=CAMERA_URL+".txt"
        	response_dict["plot"]=PLOT_URL+".png"

        
        	return HttpResponse(json.dumps(response_dict), content_type="application/json")
	else:
		return render(request, 'lsdslam/uploadVideo.html',{'title':'DesignAR'})
