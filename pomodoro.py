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
    focus_mins (int): Duration for each focus interval
    rest_mins (int): Duration for each rest interval
    interval (int): Interval count to alternate between regular and long rest
    pomo_count (int): Counter of completed pomodoro timers

    Methods
    ---------------
    start_pomo(): Start focus time for Pomodoro timer
    start_rest(): Start rest time for Pomodoro timer
    write_log(): Update the log file to track completed Pomodoros
    """

    def __init__(self, focus_mins: int, rest_mins: int, interval: int) -> None:

        # Initialize Pomodoro timer attributes based on user input
        self.focus_mins = focus_mins
        self.rest_mins = rest_mins
        self.interval = interval

        # Initialize counter attribute
        self.pomo_count = 0

    def start_pomo(self) -> None:
        """Method to start a focus timer"""

        # Find start and end time for the focus round
        self.focus_start_time = datetime.now()
        self.focus_end_time = (self.focus_start_time
                               + timedelta(minutes=self.focus_mins))

        # Start focus timer for given focus duration
        print(f'\nStarting pomodoro #{self.pomo_count + 1}...')
        for _ in tqdm(range(self.focus_mins * 60)):
            sleep(1)

        # # Increment pomodoro count and give focus completion notification
        self.pomo_count += 1
        notification.notify(
            title='Good job!',
            message=f'Take a {self.rest_mins} minute break! '
                    f'You have completed {self.pomo_count} pomodoros so far.'
        )

        # Update log file
        self.write_log(timer_type='focus',
                       start_time=self.focus_start_time.time(),
                       end_time=self.focus_end_time.time())

    def start_rest(self) -> None:
        """Method to start a rest timer"""

        # If the Pomodoro count matches the specified interval
        if self.pomo_count % self.interval == 0:
            # Rest for 3 times longer than regular rest iterations
            rest_mins = self.rest_mins * 3
        # For regular rest iterations
        else:
            # Rest for the regular rest duration
            rest_mins = self.rest_mins

        # Find start and end time for the rest round
        self.rest_start_time = datetime.now()
        self.rest_end_time = (self.rest_start_time
                              + timedelta(minutes=rest_mins))

        # Start rest timer for given rest duration
        print(f'Rest for {rest_mins} minutes...')
        for _ in tqdm(range(rest_mins * 60)):
            sleep(1)

        # Give rest completion notification
        notification.notify(
            title='Back to work!',
            message='Start another pomodro timer?'
        )

        # Update log file
        self.write_log(timer_type='rest',
                       start_time=self.rest_start_time.time(),
                       end_time=self.rest_end_time.time())

    def write_log(self, timer_type: str,
                  start_time: datetime, end_time: datetime) -> None:
        """Method to update the Pomodoro log file after each completion

        Args:
            timer_type (str): Type of either 'focus' or 'rest'
            start_time (datetime): The start time of each timer
            end_time (datetime): Tne end time of each timer
        """

        # Check if a Pomodoro log already exists
        log_file_exists = os.path.isfile('pomodoro_log.csv')

        # Create/append CSV object and add the Pomodoro record
        with open('pomodoro_log.csv', 'a', newline='') as log_f:

            fieldnames = ['date', 'type', 'start_time', 'end_time']
            writer = DictWriter(log_f, fieldnames=fieldnames)

            # Create a header row if the file is being newly created
            if not log_file_exists:
                writer.writeheader()

            # Add a row of the Pomodoro record into the log file
            writer.writerow({'date': date.today(),
                             'type': timer_type,
                             'start_time': start_time,
                             'end_time': end_time})


def main():

    # Instantiate PomodoroTimer class object
    Pomo = PomodoroTimer(focus_mins=25, rest_mins=5, interval=4)

    # Start focus and rest loop
    while True:

        Pomo.start_pomo()
        Pomo.start_rest()

        # Ask for user input for continuing Pomodoro timer
        while True:
            user_input = input('Start another Pomodoro? (Y/N): ')
            if user_input.lower() in ['y', 'n']:
                break
            else:
                print('Please enter either "Y" or "N"')

        # If the user chooses to start another Pomodoro timer
        if user_input.lower() == 'y':
            # Keep looping through the Pomo cycle
            pass
        # If the user chooses not to start another Pomodoro timer
        else:
            # Break out of the focus and rest loop
            break

    # Give final completion message
    print(f'Way to stay focused for '
          f'{Pomo.pomo_count * Pomo.focus_mins} minutes!')


if __name__ == '__main__':

    main()
