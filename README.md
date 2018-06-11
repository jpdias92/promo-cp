# promo-cp
A simple CLI program to find promotional tickets in cp.pt

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. This program was developed and tested on a macOS High Sierra, using python 3.6.5.

### Prerequisites

* Python 3 (developed using python 3.6.5). Check with `python --version` or `python3 --version`.
* [Chromedriver](http://chromedriver.chromium.org/downloads) - The web driver used. Ensure that chromedriver is in your path.

### Installing

There is an install.sh script that will start a virtual environment (venv) and install the project's dependencies, selenium and bs4. Using this script:

1. Run the install script: `./install.sh`
1. Activate the virtual environment: `source venv/bin/activate`. To stop using the venv type `deactivate`.

### Running

The program will request a search for each applicable day on cp.pt website, using the parameters specified (e.g. origin station and destination) and, after submitting a new search for each day, will print all promotional tickets found that match the specified filters.

1. You can try the program using default parameters with the command `python promo`.
1. You can check the available options and example usage with `python promo -h`.

## Built With

* [PyCharm](https://www.jetbrains.com/pycharm/) - The IDE used
* [Selenium package for python](https://pypi.org/project/selenium/) - Python language bindings for Selenium WebDriver
* [Chromedriver](http://chromedriver.chromium.org/downloads) - WebDriver for Chrome

## Authors

* **Joao Dias** - *Initial work* - [jpdias92](https://github.com/jpdias92)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

