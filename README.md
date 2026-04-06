# rotate_stl_with_aimtool
Register the specified STL model according to the marker ball positions defined in the aimtool file.

This project is used to detect spherical structures in an STL model and register them with the center coordinates of the marker balls specified in the aimtool file.

## Installation

```bash
pip install rotate_stl_with_aimtool
```

## Usage

```python
from rotate_stl_with_aimtool import rotate_stl_with_aimtool

print(
    "maximal error for tool",
    rotate_stl_with_aimtool(
        "BONE-1.stl", 
        "BONE-1.new.stl",
        "BONE-2.aimtool"
    ),
    "mm"
)
```
