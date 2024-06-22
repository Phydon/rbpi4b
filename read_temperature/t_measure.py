# use with cron job every 15 mins
import datetime as dt
import time
import os
import subprocess


FILE: str = "temperature_test.txt"
LOGS: str = os.path.join(os.path.dirname(__file__), "t_measure.log")
MAILADDRESS: str = "example@gmail.com"
# default throttling temperature on pi is 80°C
MAX_TEMP: float = 75.0


def main():
    temperature: float = get_avg_temperature()

    if too_hot(temperature):
        msg: str = f"Temperature too high: {temperature}'C"
        subject: str = "Temperature Warning Trigger"
        print(msg)
        trigger_mail(msg, subject, MAILADDRESS)


def read_temp_sensor(file: str) -> str:
    with open(file, "r") as f:
        content = f.read()

    return content


def get_avg_temperature() -> float:
    temperatures = []
    # measure every 5 seconds for 30 seconds
    for i in range(10):
        temperature: float = float(read_temp_sensor(FILE)) / 1000
        temperatures.append(temperature)
        # time.sleep(10)
        # TODO for testing -> remove later
        time.sleep(1)

    return round(sum(temperatures) / len(temperatures), 1)


def too_hot(temperature: float) -> bool:
    return True if temperature >= MAX_TEMP else False


def trigger_mail(msg: str, subject: str, mailaddress: str):
    try:
        # msg_cmd = subprocess.run(["echo", msg], check=True, capture_output=True)
        # subprocess.run(["mail", "-s", subject, mailaddress], input=msg_cmd.stdout)

        # TODO for testing ->  remove later
        raise Exception(f"Failed on purpose with: {msg}")
    except Exception as err:
        write_err_log(err, LOGS)


def write_err_log(errmsg: str, loglocation: str):
    with open(loglocation, "a+") as f:
        msg = f"{get_current_time()} :: {errmsg}"
        f.write(msg)


def get_current_time():
    return dt.datetime.now()


if __name__ == "__main__":
    main()
