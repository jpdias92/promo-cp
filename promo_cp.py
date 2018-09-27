import argparse
import calendar
import datetime
from itertools import dropwhile

from bs4 import BeautifulSoup
from selenium import webdriver

# chrome | mozilla
BROWSER = "chrome"

CP_TICKETS_PAGE = 'https://www.cp.pt/passageiros/pt/comprar-bilhetes'

ORIGIN_STATION = 'Lisboa - Oriente'
DESTINATION_STATION = 'Vila Nova de Gaia-Devesas'

MAX_TIME_RANGE = 60
HOUR_LOWER_BOUND = 16
HOUR_UPPER_BOUND = 21

PT_MONTHS = {"1": "Janeiro",
             "2": "Feveireiro",
             "3": "Março",
             "4": "Abril",
             "5": "Maio",
             "6": "Junho",
             "7": "Julho",
             "8": "Agosto",
             "9": "Setembro",
             "10": "Outubro",
             "11": "Novembro",
             "12": "Dezembro"}

APPLICABLE_WEEKDAYS = [4]

# (1)st class | (2)nd class
PASSENGER_CLASS = 2


class Service:
    def __init__(self, code=None, date=None, departure=None, arrival=None, price=None, promo_price=None):
        self.code = code
        self.date = date
        self.departure = departure
        self.arrival = arrival
        self.price = price
        self.promo_price = promo_price

    def __str__(self):
        return "Service: code: %s, date: %s %s, departure: %s, arrival: %s, price: %s, promo_price: %s" % \
               (self.code, calendar.day_name[self.date.weekday()], prepare_date_for_search(self.date), self.departure,
                self.arrival, self.price, self.promo_price)


def prepare_date_for_search(date):
    return str(date.day) + " " + str(PT_MONTHS.get(str(date.month))) + ", " + str(date.year)


def get_applicable_dates_in_range(n_days, applicable_weekdays):
    applicable_dates = []
    date = datetime.datetime.now()
    for i in range(n_days):
        date += datetime.timedelta(days=1)
        if date.weekday() in applicable_weekdays:
            applicable_dates.append(date)

    return applicable_dates


def init_web_driver(browser):
    if browser == "chrome":
        return init_web_driver_chrome()
    elif browser == "mozilla":
        return init_web_driver_mozilla()
    else:
        return None


def init_web_driver_chrome():
    options = webdriver.ChromeOptions()

    options.add_argument('headless')
    # options.add_argument("--incognito")

    # set the window size
    options.add_argument('window-size=1200x600')

    # These 2 options are needed to run headless Chrome inside a docker container, otherwise an error was thrown along the lines of:
    # selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: exited abnormally
    # (unknown error: DevToolsActivePort file doesn't exist)
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')

    # initialize the driver
    driver = webdriver.Chrome(chrome_options=options)

    return driver


def init_web_driver_mozilla():
    driver = webdriver.Firefox()

    return driver


def submit_ticket_form(web_driver, from_station, to_station, passenger_class, date):
    estacao_partida = web_driver.find_element_by_name('textBoxPartida')
    estacao_partida.send_keys(from_station)

    estacao_chegada = web_driver.find_element_by_name('textBoxChegada')
    estacao_chegada.send_keys(to_station)

    data_partida = web_driver.find_element_by_name('departDate')
    data_partida.clear()
    data_partida.send_keys(prepare_date_for_search(date))

    web_driver.execute_script("setClass(%d)" % passenger_class)

    print("Searching for %s, route %s to %s, class %d" % (date.date(), from_station, to_station, passenger_class))

    data_partida.submit()


def save_text_in_file(text):
    f = open("test.txt", "w+")
    f.write(text)
    f.close()


def parse_search_result(search_page_source, date):
    soup = BeautifulSoup(search_page_source, "html.parser")

    lines = soup.get_text().replace("\t", "").replace(" ", "").split("\n")

    lines = filter(lambda x: x.strip("\n"), lines)
    lines = dropwhile(lambda x: x != "Serviços: ", lines)

    services = []
    service = None

    for line in lines:
        if "Serviços" in line:
            if service is not None:
                services.append(service)

            service = Service(date=date)
            continue

        elif line[:2] == "IC" or line[:2] == "AP":
            service.code = line

        elif "Partida" in line:
            service.departure = line.split(":")[1] + ":" + line.split(":")[2]

        elif "Chegada" in line:
            service.arrival = line.split(":")[1] + ":" + line.split(":")[2]

        elif line == "€" and service.price is None:
            service.price = next(lines)

        elif "BilhetePromo" in line:
            service.promo_price = next(lines)

    if service is not None:
        services.append(service)

    return services


def get_promo_next_months(web_driver, from_station, to_station, passenger_class, applicable_weekdays,
                          time_range, hour_lower_bound, hour_upper_bound):
    services = []

    for date in get_applicable_dates_in_range(time_range, applicable_weekdays):
        web_driver.get(CP_TICKETS_PAGE)
        submit_ticket_form(web_driver, from_station, to_station, passenger_class, date)
        services.extend(parse_search_result(web_driver.page_source, date))

    services = filter(lambda service: service.promo_price is not None, services)
    services = filter(lambda service: int(service.departure[1:3]) >= hour_lower_bound, services)
    services = filter(lambda service: int(service.departure[1:3]) <= hour_upper_bound, services)

    print("Results:")
    for service in services:
        print(service)


def main():
    passenger_class = PASSENGER_CLASS
    applicable_weekdays = APPLICABLE_WEEKDAYS
    time_range = MAX_TIME_RANGE
    hour_lower_bound = HOUR_LOWER_BOUND
    hour_upper_bound = HOUR_UPPER_BOUND

    # create parser object
    parser = argparse.ArgumentParser(description="A simple program to find promotional tickets in cp.pt")

    # defining arguments for parser object
    parser.add_argument("-o", "--origin", type=str, nargs=1,
                        metavar="stationName", default=ORIGIN_STATION,
                        help="The name of the origin station. Must match the name in CP website."
                             f" Default='{ORIGIN_STATION}'")

    parser.add_argument("-d", "--destination", type=str, nargs=1,
                        metavar="stationName", default=DESTINATION_STATION,
                        help="The name of the destination station. Must match the name in CP website."
                             f" Default='{DESTINATION_STATION}'")

    parser.add_argument("-c", "--passengerClass", type=int,
                        metavar="class", default=PASSENGER_CLASS,
                        help="The desired class. Possible values are (1)st class or (2)nd class"
                             f" Default={PASSENGER_CLASS}")

    parser.add_argument("-w", "--weekDay", type=int, action="append",
                        metavar="dayNumber",
                        help="Filter results for specified weekday. Monday=0, Sunday=6."
                             " Specify desired days one by one, e.g. -w 4 -w 6.")

    parser.add_argument("-r", "--timeRange", type=int,
                        metavar="dayNumber", default=MAX_TIME_RANGE,
                        help="The range of days to search for promo tickets since the current day."
                             f" Default={MAX_TIME_RANGE}")

    parser.add_argument("-hl", "--hourLowerBound", type=int,
                        metavar="hour", default=HOUR_LOWER_BOUND,
                        help="The lower bound of hours to be considered on this search."
                             f" Default={HOUR_LOWER_BOUND}")

    parser.add_argument("-hu", "--hourUpperBound", type=int,
                        metavar="hour", default=HOUR_UPPER_BOUND,
                        help="The upper bound of hours to be considered on this search."
                             f" Default={HOUR_UPPER_BOUND}")

    # parse the arguments from standard input
    args = parser.parse_args()

    origin_station = args.origin
    destination_station = args.destination
    if args.passengerClass in [1, 2]:
        passenger_class = args.passengerClass

    if args.weekDay is not None:
        applicable_weekdays = args.weekDay

    if MAX_TIME_RANGE > args.timeRange > 0:
        time_range = args.timeRange

    if 24 >= args.hourLowerBound >= 0:
        hour_lower_bound = args.hourLowerBound

    if 24 >= args.hourUpperBound >= 0:
        hour_upper_bound = args.hourUpperBound

    web_driver = init_web_driver(BROWSER)
    get_promo_next_months(web_driver, origin_station, destination_station, passenger_class, applicable_weekdays,
                          time_range, hour_lower_bound, hour_upper_bound)


if __name__ == "__main__":
    main()
