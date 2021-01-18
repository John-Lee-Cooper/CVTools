# Image Viewer

**iview** is a command line app for viewing images using open_cv.

## Installation

### Using Pip

```bash
  $ pip install image_viewer
```

### Manual

```bash
  $ git clone https://github.com/John-Lee-Cooper/image-viewer
  $ cd image-viewer
  $ python setup.py install
```

## Usage

```bash
$ iview --version
$ iview --help
$ iview -r ~/Pictures
```

![iview](https://github.com/John-Lee-Cooper/image-viewer/raw/master/image/iview1.png)

### User Interface

 Key        | Result
 :--------: | :------------------------  
 SPACE      | Go to the next image
 BACKSPACE  | Go to the previous image
 DELETE     | Delete the current image
 ENTER      | Toggle full screen
 ESCAPE     | Exit
 other      | Help screen

Holding the left mouse button down and moving the mouse will pan the image.  
Rolling the mouse wheel up and down will zoom out and in where the mouse is.

## Todo

* Pan/zoom via keypad
* Config dynamic singleton
* Requirements linux vs mac
* Display image name, size, location, date taken
* Crop
* Transition


## Written by

John Lee Cooper  
john.lee.cooper@gatech.edu