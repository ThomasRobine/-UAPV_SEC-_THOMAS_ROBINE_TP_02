# Steganograhy

Self-contained tool in Python that can be used for covert messaging. 

The tool is able to “hide” ASCII text inside PNG files.

# Launch

## Help

python3 main.py -h

## Default mode, read mode

python3 main.py -png png_image_path

## Write mode

Text read from terminal entry : python3 main.py -png png_image_path -w

Text read from arguments : python3 main.py -png png_image_path -w -t "some text"

Text read from file : python3 main.py -png png_image_path -w -f filepath