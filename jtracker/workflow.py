import yaml
import json

class Workflow(object):
    def __init__(self, workflow_yaml_file=None):
        with open(workflow_yaml_file, 'r') as stream:
            self._workflow_dict = yaml.load(stream)

        self._name = self.workflow_dict.get('workflow').get('name')
        self._version = self.workflow_dict.get('workflow').get('version')

        self._get_workflow_tasks()
        #print json.dumps(self.workflow_tasks)  # debug

        self._add_default_runtime_to_tools()


    @property
    def name(self):
        return self._name


    @property
    def version(self):
        return self._version


    @property
    def workflow_dict(self):
        return self._workflow_dict


    @property
    def workflow_tasks(self):
        return self._workflow_tasks


    def _get_workflow_tasks(self):
        tasks = self.workflow_dict.get('workflow', {}).get('tasks', {})

        # converting sub_tasks under scatter tasks to top level, this way
        # it's easier to just handle flattened one level tasks, at runtime
        # sub_tasks will be instantiated with multiple parallel tasks with
        # previously defined interations (ie, field defined in 'with_items')
        scatter_tasks = []
        sub_tasks = {}
        for t in tasks:
            if '.' in t or '@' in t:
                print "Workflow definition error: task name canot contain '.' or '@', offending name: '%s'" % t
                raise
            if tasks[t].get('scatter'): # this is a scatter task
                scatter_input = tasks[t].get('scatter', {}).get('input', {})

                # quick way to verify the syntax is correct, more thorough validation is needed
                # it's possible to support two level of nested scatter tasks,
                # for now one level only
                if not len(scatter_input) == 1 and 'with_items' in scatter_input:
                    print "Workflow definition error: invalid scatter task definition in '%s'" % t
                    raise  # better exception handle is needed

                scatter_tasks.append(t)
                # expose sub tasks in scatter task to top level
                for st in tasks[t].get('tasks', {}):
                    if '.' in t or '@' in st:
                        print "Workflow definition error: task name canot contain '.' or '@', offending name: '%s'" % st
                        raise
                    if sub_tasks.get(st):
                        print "Workflow definition error: task name duplication detected '%s'" % st
                        raise

                    sub_tasks[st] = tasks[t]['tasks'][st]
                    sub_tasks[st]['scatter'] = tasks[t]['scatter']  # assign scatter definition to under each sub task
                    sub_tasks[st]['scatter']['name'] = t  # add name of the scatter task here

        # now delete the top level scatter tasks
        for st in scatter_tasks:
            tasks.pop(st)

        # merge sub_tasks into top level tasks
        duplicated_tasks = set(tasks).intersection(set(sub_tasks))
        if duplicated_tasks:
            print "Workflow definition error: task name duplication detected '%s'" % ', '.join(duplicated_tasks)
            raise

        tasks.update(sub_tasks)

        for t in tasks:
            tool_tasked = tasks[t].get('tool')
            if not tool_tasked:
                tasks[t]['tool'] = t

        self._workflow_tasks = tasks


    def _add_default_runtime_to_tools(self):
        for t in self.workflow_dict.get('tools', {}):
            if not 'runtime' in t:  # no runtime defined in the tool, add the default one
                self.workflow_dict['tools'][t]['runtime'] = self.workflow_dict.get('workflow', {}).get('runtime')
