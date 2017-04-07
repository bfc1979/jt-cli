import os
import time
import uuid


class Worker(object):
    def __init__(self, jtracker=None, host_ip=None, host_name=None, cpu_cores=None, memory=None):
        self._jtracker = jtracker
        self._host_ip = host_ip
        self._host_name = host_name
        self._cpu_cores = cpu_cores
        self._memory = memory
        self._worker_id = 'worker.%s.%s.host.%s.%s' % (
                                                            str(int(time.time())),
                                                            str(uuid.uuid4())[:8],
                                                            self.jtracker.host_ip,
                                                            self.jtracker.host_id
                                                        )

        self._current_task = None

        self._record_local_git_path()  # more of for debugging purpose


    @property
    def jtracker(self):
        return self._jtracker


    @property
    def worker_id(self):
        return self._worker_id


    def current_task(self):
        return self._current_task


    def next_task(self):
        if self._current_task: return  # if current task exists, return None

        next_task = self.jtracker.next_task(self, timeout=None)
        if next_task:
            self._current_task = next_task
            return self._current_task
        else:
            return


    def log_task_info(self, status):
        self.current_task.log_task_info(self.current_task, info={})  # info must be dict


    def task_json(self):
        return self.current_task.task_json(self.current_task.task_file)


    def task_failed(self):
        self.current_task.task_failed(self.current_task.task_file)
        self._current_task = None


    def task_completed(self):
        self.current_task.task_completed(self.current_task.task_file)
        self._current_task = None


    def _record_local_git_path(self):
        worker_id_file = os.path.join(self.jtracker.jt_home, self.worker_id)
        with open(worker_id_file, 'w')as f:
            f.write('%s\n' % self.jtracker.gitracker.local_git_path)

