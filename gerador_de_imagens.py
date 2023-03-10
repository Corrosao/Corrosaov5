import cv2
import os

# def plot_one_box(x, img, color=None, label=None, line_thickness=3, text=None, text_area=None):
#     # Plots one bounding box on image img
#     tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
#     # color = color or [random.randint(0, 255) for _ in range(3)]
#     color = [0, 0, 255]
#     c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
#     # print(f"c1: {c1}, c2: {c2}")
#     # print(f"img.shape[0]: {img.shape[0]}, img.shape[1]: {img.shape[1]}")
#     cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)

def plot_one_box(box, img, color=None, label=None, line_thickness=None):
    # Get the coordinates of the bounding box
    xmin, ymin, xmax, ymax = box
    # Check if a color is specified
    if color is None:
        # Use blue as the default color
        color = [255, 0, 0]
    # Check if a line thickness is specified
    if line_thickness is None:
        # Use a default line thickness of 2
        line_thickness = 2
    # Draw the bounding box on the image
    # cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, line_thickness)
    cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, -1, lineType=cv2.LINE_AA)
    # cv2.rectangle(img, c1, c2, color, -1, lineType=cv2.LINE_AA)
    # Check if a label is provided
    if label is not None:
        # Get the size of the label text
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        # Calculate the coordinates for the label
        label_x = int(xmin)
        label_y = int(ymin) - int(text_size[1]) - 3
        # Check if the label will be drawn outside the image
        if label_y < 0:
            # Shift the label down so it is drawn within the image
            label_y = int(ymin) + int(text_size[1]) + 3
        # Draw the label on the image
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, line_thickness)


images = os.listdir('pitting-10/test/images')
for count, image in enumerate(images, start=1):

  print('')
  print(f"{count}: pitting-10/test/images/{image}")
  # Load the image
  img = cv2.imread(f"pitting-10/test/images/{image}")

  # Get the width and height of the image
  height_1, width_1, _ = img.shape

  label_path = f'{image}'[:-3] +'txt'
  # Open the label file
  with open(f"pitting-10/test/labels/{label_path}", "r") as f:

    # Read the lines in the file
    labels = f.readlines()

    
    # Loop through the labels
    for label in labels:
        # Split the label into coordinates
        one_line, x, y, width, height = label.split()

        # Convert the string coordinates to float values
        x = float(x)
        y = float(y)
        width = float(width)
        height = float(height)

        # print(x,y,width,height)


        # Convert the normalized coordinates to pixels
        x = int(x * width_1)
        y = int(y * height_1)
        w = int(width * width_1)
        h = int(height * height_1)
        
        print(x-(w/2), y-(h/2), x+(w/2)+2, y+(h/2)+2)
        # Draw the bounding box on the image
        # if x+(w/2)+2 and y+(h/2)+2 < 400:
        plot_one_box([x-(w/2), y-(h/2), x+(w/2)+2, y+(h/2)+2], img, color=[255, 0, 0])


  # checking if the directory demo_folder??
  # exist or not.
  if not os.path.exists("/content/Corrosaov5/output"):
  # if the demo_folder directory is not present??
  # then create it.
        os.makedirs("/content/Corrosaov5/output")
        

  cv2.imwrite(f"/content/Corrosaov5/output/{image}", img)