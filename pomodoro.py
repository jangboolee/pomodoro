from datetime import date, datetime, timedelta
from time import sleep
from csv import DictWriter
import os
from plyer import notification
from tqdm import tqdm


class PomodoroTimer:
    """
    Class to represent a single Pomodoro timer

    Attributes
    ---------------
    focus_mins: int
    rest_mins: int
    interval: int
    pomo_count: int

    Methods
    ---------------
    start_pomo()
    start_rest()
    write_log()
    """

    def __init__(self, focus_mins: int, rest_mins: int, interval: int) -> None:

        # Initialize Pomodoro timer attributes based on user input
        self.focus_mins = focus_mins
        self.rest_mins = rest_mins
        self.interval = interval

        # Initialize counter attribute
        self.pomo_count = 0

    def start_pomo(self) -> None:

        self.focus_start_time = datetime.now()
        self.focus_end_time = (self.focus_start_time
                               + timedelta(minutes=self.focus_mins))

        print(f'Starting pomodoro #{self.pomo_count}...')
        for _ in tqdm(range(self.focus_mins * 60)):
            sleep(1)

        self.pomo_count += 1

        notification.notify(
            title='Good job!',
            message=f'Take a {self.focus_mins} minute break! '
                    f'You have completed {self.pomo_count} pomodoros so far.'
        )

        self.write_log(timer_type='focus',
                       start_time=self.focus_start_time.time(),
                       end_time=self.focus_end_time.time())

    def start_rest(self) -> None:

        self.rest_start_time = datetime.now()
        self.rest_end_time = (self.rest_start_time
                              + timedelta(minutes=self.rest_mins))

        print(f'Rest for {self.rest_mins} minutes...')
        for _ in tqdm(range(self.rest_mins * 60)):
            sleep(1)

        notification.notify(
            title='Back to work!',
            message='Start another pomodro timer?'
        )

        self.write_log(timer_type='rest',
                       start_time=self.rest_start_time.time(),
                       end_time=self.rest_end_time.time())

    def write_log(self, timer_type: str,
                  start_time: datetime, end_time: datetime) -> None:

        log_file_exists = os.path.isfile('pomodoro_log.csv')

        with open('pomodoro_log.csv', 'a', newline='') as log_f:
            fieldnames = ['date', 'type', 'start_time', 'end_time']
            writer = DictWriter(log_f, fieldnames=fieldnames)

            if not log_file_exists:
                writer.writeheader()

            writer.writerow({'date': date.today(),
                             'type': timer_type,
                             'start_time': start_time,
                             'end_time': end_time})


def main():

    Pomo = PomodoroTimer(focus_mins=1, rest_mins=1, interval=4)
    Pomo.start_pomo()
    Pomo.start_rest()


if __name__ == '__main__':

    main()
