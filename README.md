# ArUco_Homography
This project uses OpenCV to place an image or video on top of an ArUco tag. 

##Overview
In my first iteration of this project, I tried using a color mask and corner detection to do this. I started by using a small blue square piece of paper as my marker. I had a lot of experience with color masking and was able to create a good mask. I then tried a couple different ways to detect the corners of the square. First, I tried using OpenCV's built in Harris Corner detection function. Although this function successfully detected the corners of the mask, it often more or less than 4 corners. For my project to work, I needed to consistently find 4 corners to prevent unwanted errors in the homography process. The next method I tried was by using Hough Line detection and using the intersecting points between the lines as my corners. This was also inconsistent in the resulting data so I scrapped that idea. The last solution I tried involving color masking was by using the x and y values of the location of white pixels in the mask. Through this method, I always got 4 points, and I was able to successfully place an image on top of the blue square.

Once I got homography to work with a color mask, I discovered some limitations of this solution. Firstly, the color mask was fairly inconsistent in finding the points properly, and it was sensitive to shadows and other objects in the background providing false positives. 

Secondly, the program could not discern the rotation of the color mask. This brought 2 issues. Whenever the edges of the rectangle were parallel to the frame of the video, it had trouble finding the corners because of using the x and y method. secondly, the image pasted on the rectangle did not always follow the rotation of the camera when turning more than 90 degrees.

After these observations, I searched for a better solution and found that ArUco markers could provide exactly what I was looking for. They are easily recognizable and are a built-in part of OpenCV. Each marker is unique and has no symmetry, which means that OpenCV can differentiate the corners of the marker regardless of its orientation. I used the 4 corners of my ArUco marker as parameters for OpenCV's homography function, and it would properly rotate my input image onto the marker. 


