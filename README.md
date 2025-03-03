<a id="readme-top"></a>

<br />
<div align="center">

<h1 align="center">Metalerator</h3>

  <p align="center">
    A procedural metalcore music generator using Python and MIDI
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

![Image](https://github.com/user-attachments/assets/45491944-46d1-46c7-b2d5-71a011c23e46)

Metalerator is a Python-based procedural music generator that creates metalcore tracks in MIDI format. It generates separate MIDIs for rhythm guitar, drums, bass, lead guitar, and ambient elements, allowing for further refinement and production in digital audio workstations.

The project uses the `midiutil` library to create MIDI files, with procedural generation algorithms to create dynamic and varied compositions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) [Python](https://www.python.org/)
- ![MIDI](https://img.shields.io/badge/MIDI-000000?style=flat&logo=midi) [MIDIUtil](https://midiutil.readthedocs.io/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these instructions to set up and run Metalerator on your local machine.

### Prerequisites

- Python 3.10+
- pip package manager
- FL Studio 20+ (or any other daw (there's an .flp project in the repository with all the tracks set up)) (optional)*
- Ample Metal Hellrazer virtual guitar plugin (palm mute trigger notes are coded for this specific plugin) (optional)*
- Any virtual bass guitar plguin (optional)*
- Any virtual drum plugin (if not Superior Drummer 3, mapping may need to be adjusted) (optional)*

\* for audio rendering
### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/metalerator.git
   cd metalerator
   ```
2. Run the `run.bat` or `run.sh` script which will install `midiutil` and run the generator.
3. The generated MIDI files will be saved in the `midis` directory.
(optional)
4. For audio rendering, you need to go to `/FL/metalerator.flp` and have all aformentioned plugins installed.
5. Drag each MIDI file into the respective playlist track and export the project as an audio file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Metalerator generates five separate MIDI tracks:

1. Rhythm Guitar
2. Drums
3. Bass
4. Lead Guitar
5. Ambient Elements

Each track is saved as a separate MIDI file in the `midis` directory. These files can be imported into any DAW for further editing and production.
There are several mp3s in the `/FL` directory for demonstration purposes.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

**Gmail** – [kravtsov2109@gmail.com](mailto:kravtsov2109@gmail.com)

**LinkedIn** – [Serhii Kravtsov](https://www.linkedin.com/in/serhii-kravtsov-/)

**Facebook** – [Serhii Kravtsov](https://www.facebook.com/dud0sinka/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
