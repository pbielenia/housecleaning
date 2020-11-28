import time
import schedule
import threading


class WeekSummarizer:
    def __init__(self):
        # schedule.every(5).seconds.do(self.summarize_week)
        # self.interval_in_seconds = 1
        # self.thread = threading.Thread(target=self.__run)
        print('Entering ctor')

    def run(self):
        # self.__run()
        print('Entering run')
        # self.thread.start()

    def join(self):
        pass
        # self.thread.join()

    def __run(self):
        counter = 0
        print('Entering __run')
        # while True:
        #     print('Entering while', counter)
        #     counter = counter + 1
        #     schedule.run_pending()
            # time.sleep(self.interval_in_seconds)

    def summarize_week(self):
        print('Summarizing the week...')
