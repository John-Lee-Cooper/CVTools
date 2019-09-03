from pathlib import Path
import numpy as np
import cv2 as cv
from open_cv.lib.ui import error


# ----------------------------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------------------------


def is_cv4():
    """ if using OpenCV 3.X, then cv2.__version__ will start with '3.' """
    return cv.__version__.startswith("4.")


# ----------------------------------------------------------------------------------------
# OPEN_CV Environment
# ----------------------------------------------------------------------------------------

DATA_PATH = Path("/home/lcooper/python/open_cv/data/")

#TODO: inline everywhere
def data_path(filename) -> Path:
    return DATA_PATH / filename


# ----------------------------------------------------------------------------------------
# GUI
# ----------------------------------------------------------------------------------------

def nothing(*arg, **kw):
    pass


def draw_str(
    image,
    target,
    string,
    color=(255, 255, 255),
    bg_color=(0, 0, 0),
    font=cv.FONT_HERSHEY_PLAIN,
    font_size=4.0,
    thickness=2,
    lineType=cv.LINE_AA,
):
    """
    To put texts in images, you need specify following things.
    
        Text data that you want to write
        Position coordinates of where you want put it (i.e. bottom-left corner where data starts).
        Font type (Check cv.putText() docs for supported fonts)
        Font Scale (specifies the size of font)
        regular things like color, thickness, lineType etc.
        For better look, lineType = cv.LINE_AA is recommended.
    """

    offset = target[0] + 1, target[1] + 1
    cv.putText(
        image, string, offset, font, font_size, bg_color, thickness, lineType=lineType
    )
    cv.putText(
        image, string, target, font, font_size, color, thickness, lineType=lineType
    )


# ----------------------------------------------------------------------------------------
# Image
# ----------------------------------------------------------------------------------------
def roi(x, y, w, h):
    return np.s_[y : y + h, x : x + w]


def neighborhood(x, y, k):
    return np.s_[y - k : y + k + 1, x - k : x + k + 1]


def imread(filename=None, mode=cv.IMREAD_COLOR):
    """
    IMREAD_COLOR = Default flag for imread. Loads color image.
    IMREAD_GRAYSCALE = Loads image as grayscale.
    IMREAD_UNCHANGED = Loads image which have alpha channels.
    IMREAD_ANYCOLOR = Loads image in any possible format
    IMREAD_ANYDEPTH = Loads image in 16-bit/32-bit else converts it to 8-bit
    """
    if filename is None:
        error(f"Failed to load image file: None")

    image = cv.imread(str(filename), mode)  # str in case filename is a Path

    if image is None:
        error(f"Failed to load image file: {filename}")

    return image


def resize(
    image,
    max_size=None,
    max_width=None,
    max_height=None,
    width=None,
    height=None,
    inter=cv.INTER_AREA,
):

    h, w = image.shape[:2]

    if max_size is not None and max(h, w) > max_size:
        if h > w:
            height = max_size
        else:
            width = max_size

    elif max_height is not None and h > max_height:
        height = max_height

    elif max_width is not None and w > max_height:
        width = max_width

    if width is None and height is None:
        return image

    if width is None:
        width = int(w * height / h)
    elif height is None:
        height = int(h * width / w)

    return cv.resize(image, (width, height), interpolation=inter)


def convert_color(color, conversion):
    if conversion:
        color = cv.cvtColor(np.uint8([[color]]), conversion)[0, 0]
    return color


def mask_image(image, mask):
    return cv.bitwise_and(image, image, mask=mask)


def auto_canny(image, sigma=0.33, aperture=3, L2_gradient=False):

    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = max(0, int((1.0 - sigma) * v))
    upper = min(255, int((1.0 + sigma) * v))
    return cv.Canny(image, lower, upper, None, aperture, L2_gradient)


def otsu_canny(image, low_mult=0.1, aperture=3, L2_gradient=False):
    thresh, _ = cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return cv.Canny(image, thresh, thresh * low_mult, None, aperture, L2_gradient)


def auto_canny2(image, detect_thresh, track_thresh, aperture=3, L2_gradient=False):
    upper, lower = np.percentile(image, (detect_thresh, track_thresh))
    return cv.Canny(image, lower, upper, None, aperture, L2_gradient)


def otsu_threshold(image, mode=cv.THRESH_BINARY):
    _, result = cv.threshold(image, 0, 255, mode | cv.THRESH_OTSU)
    return result


def edge_detection(image, kernel_size=5, canny_sigma=0.33):

    """ convert the image to grayscale, blur it, and find edges in the image """
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    # edge = cv.Canny(gray, canny_low, canny_high)
    edge = auto_canny(gray, canny_sigma)
    return edge
