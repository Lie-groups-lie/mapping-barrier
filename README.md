# mapping-barrier
A locally integrated desktop software based on Python. It provides a graphical user interface (GUI) and implements two main features which helps the user to mark the barriers on complex maps and transform it into geojson polygons for further usage.

**Extract Pixels**：Based on the specified RGB color range, the eligible pixels are extracted from the input PNG image (converted to white after extraction) and the output picture is generated. In this way, maps with fuzzy or complex elements can be extracted with clear boundaries for further editing and use.\
**Polygonize Image**：Convert the input binary PNG image (containing only black and white pixels) to a polygon and export it as a GeoJSON file. With the function of *extract pixels*,this function generating a geojson and polygon file sorted by area size, and add a blank *name* feature to every polygon to assist users in subsequent editing.

# Dependencies
This project requires the following Python libraries. Please ensure that you have the required versions (Python 3.x):

- Tkinter (usually included with Python)
- Pillow
- NumPy
- GeoPandas
- Shapely
- Rasterio
- Affine

You can install the necessary libraries using the following command:

```bash
pip install pillow numpy geopandas shapely rasterio affine
```
# Usage Instructions
**1.Download or Clone the Repository**\
Download or clone the repository to your local machine:

```bash
git clone https://github.com/Lie_groups_lie/mapping_barrier.git
```
**2.Install Dependencies**\
Follow the instructions in the "Dependencies" section to install the required libraries.

**3.Run the Program**\
After navigating to the project directory, run the main program:
```bash
python Mapping_Barrier.py
```
