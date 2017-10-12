# JTracker

JTracker is a job tracking, scheduling and execution system with client-server architecture for distributed
computational workflows. All jobs are centrally managed by a JTracker server, JTracker executors (the clients)
request jobs/tasks from the server and execute them on compute nodes the executors reside.

## Installation

JTracker client needs to be installed on a workflow task execution host. It may be a VM in a cloud environment, an
HPC node, or may be just your laptop, or all of them at the same time.

```
# clone the source code
git clone https://github.com/icgc-dcc/jtracker.git

cd jtracker

# install packages
pip3 install -r requirements.txt

# install JT client
python3 setup.py install

```

## Config JT client
You need to configure JT client so it connects to an appropriate JT server, this can be done by editing `.jt/config`.

## Run it
```
# get usage information
jt --help

# start an executor pulls jobs from job queue: 455000f1-8706-4a15-8005-355e84af6368
jt executor -q 455000f1-8706-4a15-8005-355e84af6368 -c

# for more options on executor
jt executor --help

```
