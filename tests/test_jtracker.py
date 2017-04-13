# test driven development

import json
from jtracker import JTracker
from jtracker import Worker


jt = JTracker(
                    git_repo_url = 'git@github.com:junjun-zhang/jtracker_example_workflow.git',
                    workflow_name = 'ega-file-transfer',
                    workflow_version = '0.1'
                )


print "jt.jt_home: %s" % jt.jt_home
print "jt.gitracker_home: %s" % jt.gitracker_home

worker1 = Worker(jtracker=jt)

print "worker.host_ip: %s" % worker1.host_ip
print "worker.host_id: %s" % worker1.host_id
print "worker.worker_id: %s" % worker1.worker_id
print "worker.workdir: %s" % worker1.workdir

task1 = worker1.next_task()

print "task1.name: %s" % str(task1.name)
print "task1.task_dict in JSON:\n%s" % json.dumps(task1.task_dict, sort_keys=True, indent=2)
print "task1.job.job_id: %s" % task1.job.job_id
print "task1.job.job_dict in JSON:\n%s" % json.dumps(task1.job.job_dict, sort_keys=True, indent=2)

print "worker.task.name: %s" % worker1.task.name
print "worker.task.job.job_id: %s" % worker1.task.job.job_id


worker1.task_completed()

worker1.next_task()

worker1.task_completed()



worker2 = Worker(jtracker=jt)

task2 = worker2.next_task()

worker2.task_completed()


#task3 = worker1.next_task()
#worker1.task_completed()

#task4 = worker1.next_task()
#worker1.task_completed()


#worker.log_task_info({})

#worker.task_failed()

#worker.next_task()

#worker.task_completed(timeout=None)

assert False  # just to see the debugging output
