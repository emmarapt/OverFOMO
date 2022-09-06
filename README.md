<div id="top"></div>

<!-- PROJECT LOGO -->
<br />

<div align="center">
  <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/images/Logo.png">
    <img src="images/Logo.png" alt="" width="550" height="200">
  </a>

  <h3 align="center">Adaptive Coverage Path Planning</h3>
  <p align="center">
    An Active Sensing Coverage Path Planning scheme for Precision Agriculture applications!
    <!-- <br />
    <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning"><strong>Explore the docs »</strong></a>
    <br /> -->
    <br />
    <a href="https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/gif/ezgif.com-gif-maker.gif">View Demo</a>
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

[![Product Name Screen Shot][product-screenshot]](https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/images/Logo.png)

This project deals with the path planning of a mobile robot in an active sensing coverage path planning scheme adjusting the robot's speed based on the online received information of the captured images. 
At the heart of the proposed approach lies a novel mechanism that regulates the speed of the robot in accordance with both the relative quantity of identified classes (i.e., crops and weeds) and the confidence level of such detection. 
Based on the [UNet]() architecture, a state-of-the-art deep learning segmentation model is deployed for the identification and classification of crops and weeds in the incoming images.
The overall methodology is integrated into a simurealistic pipeline utilizing [AirSim](https://github.com/microsoft/AirSim) simulator for real-time observations.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ############################################### -->
<!-- GETTING STARTED -->
## Getting Started

This is an example of how you can setup the project locally.
To get a local copy up and running follow these simple steps.

### Prerequisites

First, to run the project you should install the required system packages:
   ```sh
   pip install -r requirements.txt
   ```

Second, for the adaptive path planning approach you should download any available dataset for precision agriculture applications. 

> Note: The [ASLdataset](https://projects.asl.ethz.ch/datasets/doku.php?id=weedmap:remotesensing2018weedmap) Weed Map Dataset was used for this research.
 

### Installation

1. Clone the repo 
   ```sh
   git clone https://github.com/emmarapt/Project-Name.git
   ```
2. Install AirSim
   ```sh
   pip install AirSim
   ```
   For more information, please refer to the [Documentation](https://microsoft.github.io/AirSim/).
   
3. Download any of the available [AirSim Environments](https://github.com/microsoft/AirSim/releases) based on your OS
  
  
4. Open an AirSim environment
   
   4.1 For Windows users:
   
   Go to AirSim's environment folder and launch Unreal by running the .exe application 
   
   4.2 For Linux users:
   
   Go to AirSim's environment folder via a terminal and launch Unreal by running the .sh file 

5. Finally, navigate to project directory and run:
    ```sh
   python main.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- USAGE EXAMPLES -->
## Usage

parameters.py contains all the necessary information to run the project.

- QGIS when True, the project will read the input data representing the operational area (e.g. polygon, linestring) as QGIS format. If False, the project will read the input data straightforward from the inputVariables.json.

- turnwps_path contains the path of TurnWPs.txt file which provides a set of waypoints (path) to completely cover a Region of Interest. You can use your own path or create one using the following online instance http://choosepath.ddns.net/ . 

> Note: The list of the waypoints are formatted in [WGS84](https://gisgeography.com/wgs84-world-geodetic-system/) coordinates.

### Constant speed
- mission_type when 'constant', the robot will perform a mission with constant speed

### Adaptive speed
- mission_type when 'variable', the robot will perform a mission with adaptive speed based on the received online information

### AirSim
- initial_velocity defines the initial speed of the robot during its mission. 

> Note: If mission_type is 'constant' the speed of the robot will be always equal to initial_velocity

- distance_threshold defines a limit threshold distance  between the current location of the robot and the next waypoint

> Note: This is needed to overcome issue mentioned [here](https://github.com/microsoft/AirSim/issues/1643). It may need adjudications depending on the speed and the size of the operational area.

-  time_interval defines the time interval capture of the images

- corner_radius defines a circle around every turn-waypoint with a radius equal to its value.

> Note: This is needed so that the robot does not deviate from the original flight plan due to speed fluctuations.


For the rest parameters, you need just to replace the "path" entries with the paths in your system.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ############################################### -->
<!-- Demo-->
## Demo
Now that you have the Adaptive Coverage Path Planning method running, you can use it for dealing with Informative Path Planning problems. 
Here is a video demonstration of using this project utilizing AirSim simulator in AirSimNH environment.

![](https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/gif/demo.gif)


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

Athanasios Ch. Kapoutis - [github](https://github.com/athakapo) - athakapo@iti.gr

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ############################################### -->
<!-- REFERENCES -->
## Cite As:

(Not published yet)

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: https://github.com/emmarapt/Adaptive_Coverage_Path_Planning/blob/main/images/adaptive_flow_chart.png
