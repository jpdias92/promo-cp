# promo-cp
A simple CLI program to find promotional tickets in cp.pt

## Getting Started

Below are presented 2 alternative methods to use this program.

The first one will run the program inside a docker container and is the recommended way to use this program, since you don't have to care about meeting dependencies locally, other than having Docker installed.

The second method will get you a copy of the project up and running on your local machine. This program was developed and tested on a macOS High Sierra, using python 3.6.5.

About the usage of this program, it will request a search for each applicable day on cp.pt website, using the parameters specified (e.g. origin station and destination) and, after submitting a new search for each day, will print all promotional tickets found that match the specified filters.

### Method 1 - Running inside docker container

#### Prerequisites
* Install [Docker](https://www.docker.com/) for your OS.

#### Running

1. Pull the latest Docker image from Docker Hub, with `docker pull jpdias92/promo-cp`
   * Alternatively, build the image from the Dockerfile with `docker build -t promo-cp .`
1. Run the image you built on last step with `docker run -it promo-cp`
1. You can check the available options and example usage with `docker run promo-cp -h`


### Method 2 - Running locally

#### Prerequisites
* Python 3 (developed using python 3.6.5). Check with `python --version` or `python3 --version`.
* [Chromedriver](http://chromedriver.chromium.org/downloads) - The web driver used. Ensure that chromedriver is in your path.
* [Google Chrome](https://www.google.com/chrome/).

#### Installing
There is an install.sh script that will start a virtual environment (venv) and install the project's dependencies, selenium and bs4. Using this script:

1. Run the install script: `./install.sh`
1. Activate the virtual environment: `source venv/bin/activate`. To stop using the venv type `deactivate`

#### Running

1. You can try the program using default parameters with the command `python promo_cp.py`
1. You can check the available options and example usage with `python promo -h`

## Examples

* Search for trips from Lisboa Oriente to Vila Nova de Gaia, on Fridays, with departure time between 16h and 21h
```
docker run promo-cp -o "Lisboa - Oriente" -d "Vila Nova de Gaia-Devesas" -w 4 -hl 16 -hu 21
``` 

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The IDE used
* [Selenium package for python](https://pypi.org/project/selenium/) - Python language bindings for Selenium WebDriver
* [Chromedriver](http://chromedriver.chromium.org/downloads) - WebDriver for Chrome
* [Docker](https://www.docker.com/)

## Authors

* **Joao Dias** - [jpdias92](https://github.com/jpdias92)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

