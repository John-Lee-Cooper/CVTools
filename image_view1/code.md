## iview1

fstring
pathlib
click - demo

Ideally every module should be executable, 
with a python shebang (#!/usr/bin/env python) at the top,
and a
```
if __name__ == "__main__":
    demo()
```
at the bottom, where demo() is a short function that demostrates the modules functionality

```python
@click.command()
@click.option(
    "--size",
    type=click.IntRange(min=8),
    default=640,
    help="width or maximum height of displayed image",
)
@click.argument("paths", type=PATH, nargs=-1)
def main(paths, size):
    """
    iview1 - a digital photo viewer

    \b
    iview1 displays the image specified by PATHS.
    PATHS is a list of image paths or a directory containing images.

    iview1 allows you to step forward or backward though all the images
    and/or image directories specified in the arguments.

    \b
    Press
      <SPACE>     to go to the next image.
      <BACKSPACE> to go to the previous image.
      <DELETE>    to delete current image.
      <ESCAPE>    to exit.
    """

    if not paths:
        context = click.get_current_context()
        click.echo(context.get_help())
    else:
        iview.main(paths, size=size)
```

## click_support.py

```python
class PathParamType(click.types.Path):
    """ Click type extension that takes a path string and returns a Path """

    name = "Path"

    def __init__(self, exists: bool = True, **kw):
        super().__init__(exists=exists, **kw)

    def convert(
        self, value: str, param: click.ParamType, ctx: click.Context
    ) -> PosixPath:
        try:
            return Path(super().convert(value, param, ctx))
        except ValueError:
            self.fail("%s is not a valid path" % value, param, ctx)
```

## iview.py

```python
def process(window: Window, image_path: PosixPath, size: int) -> int:
    """
    Read image from image_path,
    resize it so that it is a width or height is size,
    and display it in window.
    Return any key strokes
    """
    image = imread(image_path)

    image = resize(image, width=size, max_size=size)

    key = window.display(image, 0)
    return key
```


```python
def main(paths: List[FilePath], size: int = 640) -> None:
    """
    Main routine
      Create window
      Create image Path list
      Display images
      Allow user to step forward and backward through list
    """

    with Window() as window:

        image_ring = paths_to_image_ring(paths)
        for image_path in image_ring:
            window.set_title(image_path.name)

            key = process(window, image_path, size)

            if key == config.NEXT_KEY:
                image_ring.forward()

            elif key == config.PREV_KEY:
                image_ring.backward()

            elif key in config.DELETE_KEY:
                trash(image_ring.pop())

            else:
                print(key_help())
```

##  window.py

```python
class Window:
    """ Class wrapper for open_cv window functions """

    def __init__(
        self, name="", flag=cv.WINDOW_GUI_NORMAL, image=None, include_script_name=True
    ):
        name = self.make_name(name)
        if not name or include_script_name:
            name = f"{script_name()} {name}"
        self.name = name
        cv.namedWindow(self.name, flag)
        cv.setWindowProperty(self.name, cv.WND_PROP_AUTOSIZE, 1.0)

        self.mouse_down = False
        self.r_mouse_down = False
        self.mouse_at = self.mouse_down_at = None
        self.r_mouse_at = self.r_mouse_down_at = None
        self.mouse_down_with = None
        self.r_mouse_down_with = None

        if image is not None:
            self.display(image)

    def destroy(self):
        """ Remove the window """
        cv.destroyWindow(self.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    @staticmethod
    def make_name(name: FilePath) -> Optional[PosixPath]:
        """ If name is a PosixPath, return its name, else assume its a string and return it """
        return Path(name).name if isinstance(name, PosixPath) else name

    def set_title(self, title: FilePath, include_script_name: bool = True) -> None:
        """ Set the title of the window """
        title = self.make_name(title)
        if include_script_name:
            title = f"{script_name()} {title}"
        cv.setWindowTitle(self.name, title)

    def move(self, x: int, y: int) -> None:
        """ Move the window to x, y """
        cv.moveWindow(self.name, x, y)

    def display(
        self, image: Image, wait_ms: int = None, title: Optional[FilePath] = None
    ) -> int:
        """
        Display image in window

        By default it will wait for ever for a key stroke
        If wait is None, it will not wait at all.
        """
        if title:
            self.set_title(title)

        cv.imshow(self.name, image)

        if wait_ms is None:
            return -1  # None

        return self.wait(wait_ms)

    @staticmethod
    def wait(wait_ms: int = 0) -> int:
        """ Wait for a keystroke or until wait_ms milliseconds pass """

        key_code = cv.waitKey(int(wait_ms))
        # = cv.waitKeyEx(int(wait_ms))

        if key_code & 0xFF == ESC_KEY:
            sys.exit(0)

        return key_code
```

##  image_paths.py

```python
# imread supports
IMAGE_EXTS = ".bmp .dib .jpeg .jpg .jpe .jp2 .webp .png .pbm .pgm .ppm .pxm .pnm .pfm .sr .ras .tif .tiff .exr .hdr .pic".split(
    " "
)
```


```python
def imread(file_name: FilePath, flags: int = cv.IMREAD_COLOR) -> Image:
    """
    Load an image from the specified file and returns it.
    Filename may be a Path.

    flags may be:
      IMREAD_COLOR = Default flag for imread. Loads color image.
      IMREAD_GRAYSCALE = Loads image as grayscale.
      IMREAD_UNCHANGED = Loads image which have alpha channels.
      IMREAD_ANYCOLOR = Loads image in any possible format
      IMREAD_ANYDEPTH = Loads image in 16-bit/32-bit else converts it to 8-bit
    """
    image = cv.imread(str(file_name), flags)  # str in case file_name is a Path

    if image is None:
        ui.error(f"Failed to load image file: {file_name}")

    return image
```


```python
def imwrite(
    file_name: FilePath,
    image: np.ndarray,
    dir_path: Optional[FilePath] = None,
    params: Optional[int] = None,
) -> None:
    """
    Save image to file_name
    Filename may be a Path.
    If dir_path is provided, save image in that directory
    """
    if dir_path:
        file_name = Path(dir_path).parent / Path(file_name).name
    cv.imwrite(str(file_name), image, params)
```


```python
def paths_to_image_ring(
    paths: List[FilePath], subdirectories: bool = True
) -> RingBuffer:
    """ Return a RingBuffer of image Paths given a list of file and/or directory Paths """

    if len(paths) == 0:
        ui.warning(f"paths_to_image_paths(paths): paths is empty")
        return RingBuffer([])

    if len(paths) == 1:
        return path_to_image_ring(paths[0], subdirectories)

    image_paths_ = []
    for index, path in enumerate(paths):
        path = Path(path)
        if is_image_path(path):
            image_paths_.append(path)
        else:
            ui.warning(f"paths_to_image_paths(paths): paths[{index}] is not an image")

    if not image_paths_:
        ui.warning(f"No images in {paths}")
    return RingBuffer(image_paths_)
```


```python
def path_to_image_ring(path: FilePath, subdirectories: bool = True) -> RingBuffer:
    """ Return a RingBuffer of image Paths given a file or directory Path """
    path = Path(path)
    pattern = "**/*" if subdirectories else "*"

    if path.is_dir():
        image_ring = RingBuffer(image_paths(path, pattern))
    elif is_image_path(path):
        image_ring = RingBuffer(image_paths(path.parent, pattern), path)
    else:
        ui.warning(
            f"path_to_image_paths(path): path:{path} is not a directory or image"
        )
        return RingBuffer([])

    if not image_ring:
        ui.warning(f"No images in {path}")
    return image_ring
```


```python
def is_image_path(path: PosixPath) -> bool:
    """ Return if path is a valid path for an image"""
    return path.is_file() and path.suffix.lower() in IMAGE_EXTS
```


```python
def image_paths(directory_path: str = ".", pattern: str = "*") -> List[PosixPath]:
    """
    Return the paths to the images in directory_path that matches the pattern.
    """
    return file_paths(directory_path, pattern=pattern, valid_exts=IMAGE_EXTS)
```

## paths.py

```python
def script_name() -> str:
    """ Return final path component of script without .py extension """
    return Path(argv[0]).stem
```


```python
def trash(path: FilePath) -> None:
    """
    Move path to trash directory (safe delete)
    If path already exists there, try adding a number (1) to the end of the name
    and increment it until a unique path is found.
    """
    src_path = Path(path)
    dst_path = config.TRASH_PATH / src_path.name

    # Ensure we are not overwriting anything in trash
    count = 1
    while dst_path.exists():
        count += 1
        dst_path = dst_path.parent / f"{dst_path.stem}_{count}{dst_path.suffix}"

    src_path.replace(dst_path)
```


```python
def file_paths(
    directory_path: FilePath, pattern: str = "*", valid_exts: Optional[List[str]] = None
) -> List[PosixPath]:
    """
    Yield the next path in directory_path that matches the pattern and
    if specified, has a suffic contained in valid_exts
    """
    directory_path = Path(directory_path)
    assert directory_path.is_dir()

    # if filename does not end in valid_ext, ignore it
    result = [
        path
        for path in directory_path.glob(pattern)
        if valid_exts is None or path.suffix.lower() in valid_exts
    ]

    result.sort()
    return result
```

## ring_buffer.py

```python
class RingBuffer:
    """
    Generic circular buffer.

    >>> ring = RingBuffer("abc", "b")
    >>> ring.forward()
    >>> str(ring)
    "RingBuffer(['a', 'b', 'c'], 'b')"
    >>> next(ring)
    'c'
    >>> next(ring)
    'a'
    >>> ring.backward()
    >>> next(ring)
    'c'
    """

    def __init__(self, list_: Union[Sequence, Iterator], value: Any = None):
        self._step = 0
        self._list = list(list_)
        self._index = 0 if value is None else self._list.index(value)

    def __repr__(self):
        return f"RingBuffer({self._list}, {repr(self.value())})"

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._list:
            return  # stops iteration

        self._index = (self._index + self._step) % len(self._list)
        return self._list[self._index]

    def value(self) -> Any:
        """
        Return the current item in the list

        >>> ring = RingBuffer("abc", "b")
        >>> ring.value()
        'b'
        """
        if not self._list:
            raise StopIteration
        return self._list[self._index]

    def next(self) -> Any:
        """ Advance ringbuffer index forward """
        self._index = (self._index + 1) % len(self._list)
        return self._list[self._index]

    def prev(self) -> Any:
        """ Advance ringbuffer index backward """
        self._index = (self._index - 1) % len(self._list)
        return self._list[self._index]

    def forward(self) -> None:
        """ Cause ringbuffer next call to __next__ to advance forward """
        self._step = 1

    def backward(self) -> None:
        """ Cause ringbuffer next call to __next__ to advance backward """
        self._step = -1

    def stop(self) -> None:
        """ Cause ringbuffer next call to __next__ to not advance """
        self._step = 0

    def pop(self) -> Any:
        """
        Remove the current item in the list and return it.

        >>> ring = RingBuffer("abcd", "c")
        >>> ring.pop()
        'c'
        >>> str(ring)
        "RingBuffer(['a', 'b', 'd'], 'b')"
        >>> ring.backward()
        >>> ring.pop()
        'b'
        >>> str(ring)
        "RingBuffer(['a', 'd'], 'd')"
        """
        result = self._list[self._index]
        del self._list[self._index]
        if self._step >= 0:
            self._index -= 1
        return result
```

## image_utils.py

```python
def resize(
    image: Image,
    height: Optional[int] = None,
    width: Optional[int] = None,
    max_size: Optional[int] = None,
    max_height: Optional[int] = None,
    max_width: Optional[int] = None,
    interpolation: int = cv.INTER_AREA,
) -> Image:
    """
    Return image scaled using interpolation.
    The new size can be specified using height or width.
    The size can be further specified using max_width, max_height or max_size.
    The result will always have the same aspect ratio.

    >>> image = np.zeros([50, 100], dtype=np.uint8)
    >>> image.shape
    (50, 100)
    >>> resize(image, height=100).shape
    (100, 200)
    >>> resize(image, max_size=80).shape
    (40, 80)
    >>> resize(image, max_height=30).shape
    (30, 60)
    """

    assert height is None or width is None
    assert (max_size is not None) + (max_height is not None) + (
        max_width is not None
    ) <= 1

    h, w = image.shape[:2]
    if height is not None:
        width = int(w * height / h)
    elif width is not None:
        height = int(h * width / w)
    else:
        height, width = h, w

    if max_size is not None and max(height, width) > max_size:
        if height > width:
            height = max_size
            width = int(w * height / h)
        else:
            width = max_size
            height = int(h * width / w)

    elif max_height is not None and height > max_height:
        height = max_height
        width = int(w * height / h)

    elif max_width is not None and width > max_height:
        width = max_width
        height = int(h * width / w)

    if width == w and height == h:  # No change
        return image

    # To shrink an image, it will generally look best with INTER_AREA.
    # To enlarge an image, it will generally look best with INTER_CUBIC interpolation.
    if interpolation is None:
        interpolation = cv.INTER_AREA if width <= w else cv.INTER_CUBIC

    return cv.resize(image, (width, height), interpolation=interpolation)
```
