# Astrotracker

Astrotracker is a Python-based tool for astronomical event tracking and visualisation.  
It provides an interactive interface to compute, plot, and analyse celestial positions of Sun, Moon, planets, and stars
using PyQt6 and Plotly.

---

## Features

- **Built-in database of celestial objects and cities (expandable)**  
  Comes with a default set of stars, planets, and cities. You can add more objects or locations as needed.

- **Track trajectories for Sun, Moon, planets, and stars**  
  Compute and visualise the path of any celestial object over a selected date and location.

- **View trajectories in Azimuth/Altitude or Equatorial coordinates**  
  Choose between local sky coordinates (Az/Alt) or universal Equatorial coordinates for analysis.

- **Multi data options**  
  Track multiple objects at once, monitor the same object from different locations, or analyse it over multiple days.

- **Time options: Civil, Local Astronomical, and Greenwich Time**  
  Display object positions in your preferred time format for accuracy and convenience.

- **Save results to CSV**  
  Export the computed data for further analysis or record-keeping.

- **Interactive, high-quality Plotly graphs**  
  Explore celestial trajectories with zoomable, interactive plots.

- **Export graphs as PNG**  
  Save visualisations as images for reports or presentations.

---

## Source Code

### Download

To clone the repository:
```bash
git clone https://github.com/panta1978/astrotracker
cd astrotracker
```

### Installation

Ensure you have **Python 3.13** installed.
Other Python versions may work, but they have not been thoroughly tested.

Install the required dependencies:
```bash
pip install -r requirements.txt
```

To compile the version from the source code, run compile.bat (Windows only).

---

## Executable

If you are using Windows and prefer a standalone executable, check the Releases section for .exe builds.
Latest version is available at [this link](https://github.com/panta1978/astrotracker/releases/latest).
Note. To free up space, previous versions' executables files might not be kept.

---

## Versioning and License

Astrotracker is distributed under the **MIT License** starting from **v1.1**.

MIT License © 2025 Stefano Pantaleoni  
See [LICENSE.txt](LICENSE.txt) for full terms.
