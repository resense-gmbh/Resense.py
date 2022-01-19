Python library for interfacing with the WITTENSTEIN HEX force/torque sensors.

## Dependencies

Resense.py requires the installation of the following libaries: `pyserial`, `numpy`, `matplotlib`

## Installation

Install Resense.py using the following commands:

- `git clone https://github.com/WSE-Resense/Resense.py`
- `cd Resense.py`
- `pip install .`

## Usage

The library consists of five submodules. The following three are imported by default using `import resensepy`:

- `recording`: Contains classes to store and work with recordings and recording sets
- `importer`: Load recordings from files using *CSV*, *JSON* or *FTE Binary* file format
- `exporter`: Save recordings to files using *CSV* file format (other formats are not supported)

The following modules have to be imported manually:

- `from resensepy import sensor`: Connect to an electronisc box using USB and record the incoming F/T-data
- `from resensepy import visualizer`: Display recordings as basic force/torque plots using matplotlib and pyplot

## License notice

Resense.py was written by Elias Hörner. Please send questions/issues about/with the Python library to (elias.hoerner@wittenstein.de).