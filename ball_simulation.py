import math

class Ball:

    def __init__(self,
            circle_center, moment_center, radius, color, hsv):
        self.circle_center = circle_center
        self.moment_center = moment_center
        self.radius = radius
        self.color = color
        self.hsv = hsv
        self.x = circle_center[0] # sort by this value
        self.y = circle_center[1]

    """
    Get the center of the ball that is identified by the hsv values.
    Note: This uses cv2.minEnclosingCircle(). This result can be
    different by several pixels from the moment center. The difference
    between these two methods is documented at https://docs.opencv.org/3.1.0/d3/dc0/group__imgproc__shape.html#ga8ce13c24081bbc7151e9326f412190f1.
    """
    def get_circle_center(self):
        return self.circle_center

    """
    Get the center of the ball that is identified by the hsv values.
    Note: This uses cv2.moments(c) to calculate the center pixel of
    the ball. This will always an integer pair.
    The difference between these two methods is documented at https://docs.opencv.org/3.1.0/d3/dc0/group__imgproc__shape.html#ga8ce13c24081bbc7151e9326f412190f1.
    """
    def get_moment_center(self):
        return self.moment_center

    def get_radius(self):
        return self.radius

    def get_color(self):
        return self.color

    def get_hsv(self):
        return self.hsv

    def __str__(self):
        return str(self.color) + " : " + str(self.get_circle_center())

    def __repr_(self):
        return repr((self.color, self.get_circle_center()))

class Frame:
    """
    Starts the calculations done to locate the balls in the frame.
    :param frame: numpy array that is provided from cv2:VideoCapture:read()
    :param color_range: a dictionary in the form of
    {color_identifier : (hsv_min, hsv_max) } as calculated from
    range-detector.py
    :param frame_count: optional interger used to describe the frame number
    """
    def __init__(self, frame, color_range, servo_angle=0,
        target_spacing=1, camera_ratio=0.0189634, frame_count=0):
        self.frame = frame
        self.color_range = color_range
        self.servo_angle = servo_angle
        self.target_spacing = target_spacing
        self.camera_ratio = camera_ratio

    def calculate_xyr(self, balls):
        ordered_balls = sorted(balls, key=lambda ball: ball.x)
        angle1 = self.camera_ratio * math.sqrt((balls[0].x - balls[1].x) ** 2 + (balls[0].y - balls[1].y) ** 2)
        angle2 = self.camera_ratio * math.sqrt((balls[1].x - balls[2].x) ** 2 + (balls[1].y - balls[2].y) ** 2)
        num = self.target_spacing * math.sin(angle1 + angle2)
        den = (self.target_spacing * math.sin(angle2) / math.sin(angle1)) - (self.target_spacing * math.cos(angle1+angle2))
        alpha = math.atan(num/den)
        l = self.target_spacing * math.sin(angle1 + alpha) / math.sin(angle1) # length from ball to robot
        x = l * math.sin(alpha)  #x from right-most ball
        y = -l * math.cos(alpha)  #y from right-most ball (ball[2]). Add constants if you want the origin as shown in picture
        rotOffset = (balls[1].x - 1640) * self.camera_ratio
        rotation = self.servo_angle + rotOffset + alpha + 90
        return(x,y,rotation)


#Supplemental function for sorted function. Returns xCord.
#def get_x_cor(ball):
#    return ball.circle_center[0]

if __name__ == "__main__":
    green_ball = Ball((100,300), (101, 301), 100, "Green", None)
    red_ball = Ball((300,300), (301, 301), 100, "Red", None)
    blue_ball = Ball((500,300), (501, 301), 100, "Blue", None)

    balls = [green_ball, blue_ball, red_ball]

    frame = Frame(None, None, 0, 0.825)


    print green_ball

    print "Unsorted-",balls
    print balls[0],balls[1],balls[2]

    #Makes a sorted list of balls based on their xcors
    #sorted_list = sorted(balls,key = x)
    sorted_list = sorted(balls, key=lambda ball: ball.x)
    print "Sorted-",sorted_list
    print sorted_list[0],sorted_list[1],sorted_list[2]


    print("Calculation")
    print(frame.calculate_xyr(balls))

    #Sort ball by x value
