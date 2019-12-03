import json
from datetime import datetime
import time
import subprocess
import croniter
import sys
import threading


class Scheduler:
    def __init__(self, json_strobj=None):
        if not json_strobj or json_strobj == "":
            print("No jobs")
            exit()
        if isinstance(json_strobj, str):
            self._tasks = json.loads(json_strobj)
        else:
            self._tasks = json_strobj
        self._storage = dict()
        self.fill_storage()
        print("Start jobs scheduling on " + str(datetime.now()))
        print("Jobs count: " + str(len(self._storage)))
        self.run()

    def fill_storage(self):
        now_time = datetime.now()
        for task, data in self._tasks.items():
            cron = croniter.croniter(data["time"], now_time)
            next_time = {"next": cron.get_next(datetime).strftime("%Y-%m-%d %H:%M")}
            self._storage[task] = {**data, **next_time}

    def run(self):
        try:
            python = "python"
            if sys.version_info.major < 3:
                python = "python3"
            while True:
                format_now_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                for task, data in self._storage.items():
                    if data["next"] == format_now_time:
                        self._storage[task]["next"] = \
                            croniter.croniter(data["time"], datetime.now()).get_next(datetime).strftime(
                                "%Y-%m-%d %H:%M")
                        print("Start task: " + str(task))
                        subprocess.Popen([python, data["command"] + '.py'])
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopped")
            exit()


if __name__ == "__main__":
    js = {
        "task1": {"time": "* * * * *", "command": "/home/evg/PycharmProjects/scheduler/scheduler_scripts/printer"},
        "task2": {"time": "* * * * *", "command": "/home/evg/PycharmProjects/scheduler/scheduler_scripts/tester"}
    }
    s = Scheduler(js)
