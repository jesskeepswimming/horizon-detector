 							
# Instructions for running code
My code is written in Python 3.9. Please run it like this:
> python3 run.py --input name_of_input_folder --output name_of_output_folder

Note that the --output argument is optional. If no output folder is passed in, the code will create a new unique folder and print its name into the console.

Please install the following dependencies:
- open-cv or opencv-python
- matplotlib
- tqdm

# A brief explanation of how your code works
 							
The code first preprocesses the images using a Canny edge detector. Then, a Standard Hough Line transform is applied to the resulting image to detect straight lines in the image. From the outputs of this function, the longest line is chosen as the horizon line. Using the point-slope form equation, this line is extended to meet the left and right borders of the image.

Figure 1: Result of Canny Edge Detector and straight lines detected by the Hough Transform  


Figure 2: The longest line picked and extended to cover the image.

This approach assumes that the horizon would be the straightest/longest line in the image. Given that drone footage is most often taken from a high point and over fairly natural scenery, this is an appropriate assumption given that the longest and greatest contrast across a frame occurs where land/sea meets the sky.  

# Evaluation metrics

Finally, the evaluation metric I have chosen is the mean and standard deviation of how vertically far apart each endpoint (leftmost and rightmost) is from their respective ground truth points. I halve the sum of the left and right difference to get an approximation of the average number of pixels away each estimate is from the ground truth. 

Cost = (|y_left - y_ground_truth_left| + |y_right - y_ground_truth_right|)/2

This cost is very simple and fast to compute, and the final metric gives the average and the standard deviation of the distances in pixels. Here are the final results 

For input_1:
Mean:  49.21333333333333
Standard Deviation:  43.528930864681506

For input_2:
​​Mean:  62.53
Standard Deviation:  70.67189988484344