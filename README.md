<div id="top"></div>

<!-- PROJECT LOGO -->
<br />

<div align="center">

  
  <a href="https://raw.githubusercontent.com/emmarapt/Adaptive_Coverage_Path_Planning/main/images/visual_abstract.png?token=GHSAT0AAAAAABYET72HGAKC25R6RHBLGKDSYZENJEA">
    <img src="https://raw.githubusercontent.com/emmarapt/Adaptive_Coverage_Path_Planning/main/images/visual_abstract.png?token=GHSAT0AAAAAABYET72HGAKC25R6RHBLGKDSYZENJEA" alt="" width="1000" height="">
  </a>

  <h3 align="center">Adaptive Coverage Path Planning</h3>
  <p align="center">
    An Active Sensing Coverage Path Planning scheme for Precision Agriculture applications!
    <!-- <br />
    <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning"><strong>Explore the docs »</strong></a>
    <br /> -->
    <br />
    <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/gif/demo.gif">View Demo</a>
    ·
    <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/issues">Report Bug</a>
    ·
    <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/issues">Request Feature</a>
  </p>
</div>


<!-- ############################################### -->
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#qualitative-results">Qualitative Results</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    <li><a href="#cite-as">References</a></li>
  </ol>
</details>


<!-- ############################################### -->
<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![product-screenshot]](https://raw.githubusercontent.com/emmarapt/Adaptive_Coverage_Path_Planning/main/images/adaptive_pipeline.png?token=GHSAT0AAAAAABYET72HHW34TQECP5O5LUGIYZENLLA) -->
<div align="center">
  <a href="https://raw.githubusercontent.com/emmarapt/Adaptive_Coverage_Path_Planning/main/images/adaptive_pipeline.png?token=GHSAT0AAAAAABYET72HHW34TQECP5O5LUGIYZENLLA">
    <img src="https://raw.githubusercontent.com/emmarapt/Adaptive_Coverage_Path_Planning/main/images/adaptive_pipeline.png?token=GHSAT0AAAAAABYET72HHW34TQECP5O5LUGIYZENLLA" alt="" width="1000" height="">
  </a>
</div>
This project deals with the path planning of a mobile robot in an active sensing coverage path planning scheme adjusting the robot's speed based on the online received information of the captured images. 
At the heart of the proposed approach lies a novel mechanism that regulates the speed of the robot in accordance with both the relative quantity of identified classes (i.e., crops and weeds) and the confidence level of such detection. 
A state-of-the-art deep learning segmentation model is deployed for the identification and classification of crops and weeds in the incoming images.
The overall methodology is integrated into a simurealistic pipeline utilizing [AirSim](https://github.com/microsoft/AirSim) simulator for real-time reactions and observations.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ############################################### -->
<!-- GETTING STARTED -->
## Getting Started

This is an example of how you can setup the project locally.
To get a local copy up and running follow these simple steps.

### Prerequisites

**Step 1. To run the project you should install the required system packages:**
   ```sh
   pip install -r requirements.txt
   ```
> Note: TensorFlow version for CPU & GPU support may differ based on your system requirements.

**Step 2. Install [CUDA](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html) based on your system requirements (For GPU support).**

**Step 3. Install GDAL.**

   1. Download a pre-built [gdal wheel file](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
   
   > Note: You’ll need to select the file that matches your specific Python version and operating system (32 or 64 bit).
    
   2.   Install the wheel file with pip
  
   ```sh
   python -m pip install path-to-wheel-file.whl
   ```
   Assuming that you’ve used the appropriate wheel file, this should successfully install gdal.
    
   If you use anaconda environment, please follow the [tutorial for installing gdal with conda](https://opensourceoptions.com/blog/how-to-install-gdal-with-anaconda/).

<!-- **Step 3. Install TensorFlow for CPU & GPU support based on your system requirements.** -->

**Step 4. For the adaptive path planning approach you should download any available dataset for precision agriculture applications.** 

> Note: The Weed Map [ASLdataset](https://projects.asl.ethz.ch/datasets/doku.php?id=weedmap:remotesensing2018weedmap) was used for this research.
 

### Installation

1. Clone the repo 
   ```sh
   git clone https://github.com/emmarapt/Adaptive_Coverage_Path_Planning.git
   ```
   
2. Download any of the available [AirSim Environments](https://github.com/microsoft/AirSim/releases) based on your OS
  
3. Open an AirSim environment
    
   * *3.1 For Windows users:*
   
   Go to AirSim's environment folder and launch Unreal by running the .exe application. 
   
   * *3.2 For Linux users:*
   
   Go to AirSim's environment folder via a terminal and launch Unreal by running the .sh file.

4. Navigate to project directory via a terminal and run:
    ```sh
   python main.py
   ```
   
5. Follow the message for Take-off:

   ```sh
   Press any key to takeoff
   ```
   
  Enjoy the flight! <img src="https://cdn-icons-png.flaticon.com/512/72/72592.png" alt="" width="40" height="40">


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- USAGE EXAMPLES -->
## Usage

parameters.py contains all the necessary information to run the project.

- QGIS when True, the project will read the input data representing the operational area (e.g. polygon, linestring) as QGIS format. If False, the project will read the input data straightforward from the inputVariables.json.

- turnwps_path contains the path of TurnWPs.txt file which provides a set of waypoints (path) to completely cover a Region of Interest. You can use your own path or create one using the following online instance http://choosepath.ddns.net/ . 

> Note: The list of the waypoints are formatted in [WGS84](https://gisgeography.com/wgs84-world-geodetic-system/) coordinates.

### Dataset
- ortho_georef_img contains the path entry of the .tif field image within the dataset's folder 
- ortho_rgb_img contains the path entry of the .png field image within the dataset's folder 

### Constant speed
- mission_type when 'constant', the robot will perform a mission with constant speed

### Adaptive speed
- mission_type when 'variable', the robot will perform a mission with adaptive speed based on the received online information

### AirSim
- initial_velocity defines the initial speed of the robot during its mission

> Note: If mission_type is 'constant' the speed of the robot will be always equal to initial_velocity

- distance_threshold defines a limit threshold distance between the current location of the robot and the next waypoint

> Note: This is needed to overcome issue mentioned [here](https://github.com/microsoft/AirSim/issues/1643). It may need adjudications depending on the speed and the size of the operational area.

- time_interval defines the time interval capture of the images

- corner_radius defines a circle around every turn-waypoint with a radius equal to its value

> Note: This is needed so that the robot does not deviate from the original flight plan due to speed fluctuations.


For the rest parameters, you just need to replace the "path" entries to match with the paths in your operating system.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ############################################### -->
<!-- Demo-->
## Demo
Now that you have the Adaptive Coverage Path Planning method running, you can use it for dealing with Informative Path Planning problems. 
Here is a video demonstration of using this project utilizing AirSim simulator in AirSimNH environment.

<div align="center">
  <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/gif/demo.gif">
    <img src="gif/demo.gif" alt="" width="650" height="350">
  </a>
</div>


<!-- ############################################### -->
<!-- Qualitative Results -->
## Qualitative Results
To validate the efficiency of the Adaptive Coverage Path Planning method we evaluate the generated orthomosaic maps in terms of image quality. 
Towards this direction, simulated missions deployed with the baseline and the active sensing method are conducted for the field "002" of the Weedmap [ASLdataset](https://projects.asl.ethz.ch/datasets/doku.php?id=weedmap:remotesensing2018weedmap), with nominal speed of 3 m/s. 

<div align="center">
  <a href="https://raw.githubusercontent.com/emmarapt/Adaptive_Coverage_Path_Planning/main/images/Qualitative_Results.png?token=GHSAT0AAAAAABYET72H5R7UH6IAIHJB3LYMYZENNUA">
    <img src="https://raw.githubusercontent.com/emmarapt/Adaptive_Coverage_Path_Planning/main/images/Qualitative_Results.png?token=GHSAT0AAAAAABYET72H5R7UH6IAIHJB3LYMYZENNUA" alt="" width="900" height="">
  </a>
</div>

<!-- ############################################### -->
<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- LICENSE -->
## License

Distributed under the MIT License. See [LICENSE](https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- CONTACT -->
## Contact

Marios Krestenitis - [github](https://github.com/wave-transmitter) - mikrestenitis@iti.gr

Emmanuel K. Raptis - [github](https://github.com/emmarapt) - emmarapt@iti.gr

Athanasios Ch. Kapoutsis - [github](https://github.com/athakapo) - athakapo@iti.gr

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
This research has been financed by the European Regional Development Fund of the European Union and Greek national funds through the Operational Program Competitiveness, Entrepreneurship and Innovation, under the call RESEARCH - CREATE - INNOVATE (T1EDK-00636).
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- REFERENCES -->
## Cite As:

(Not published yet)

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/images/adaptive_pipeline.png