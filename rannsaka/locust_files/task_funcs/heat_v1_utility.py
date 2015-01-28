import os
import random
import time
import json

from locust import HttpLocust, TaskSet, task

import keystone_v2_base as keystone_base
import heat_v1_base as heat_base

""" These are more complex 'tasks' built, upon the base api tasks.
    They are intended to be a write-once, re-use-many resource and
    to provide the building blocks for task-sets / test runs.

"""

def abandon_and_adopt_stack(self):
    """ Designed to randomly select a stack,
        abandon it, save the data from the call,
        then re-adopt it.

        Intended to allow for collisions and messiness.
        This is for bug-hunting. 

    """
 
    stack_name, stack_id = heat_base.get_stack_name_and_id(self)
    response = heat_base.abandon_stack(self,
                                       stack_name=stack_name,
                                       stack_id=stack_id)
    response = json.loads(response.content)
    self.output("abandon_adopt_RESPONSE:")
    self.output(response)
    template = response['template']
    resources = response['resources']


def create_stack(self):
    """ We use this method to help handle the particulars
        of our basic test scenarios.  Tailored to basic
        test stack creation for templates in etc dir.

    """
    
    params = {}
    disable_rollback=True

    # stack name
    stack_name = "stack-%s-%s" % (self.id, self.stack_count)
    self.stack_count += 1

    # generate timeout
    timeout_mins = 30 # general default / maybe leave None(?)
    if self.one_in_ten():
        timeout_mins = random.choice([0,0,0,1,1,5,5,10,10,10,15,20,100,-1,'zebra golfcart tango',10000000000000000, .5])
    # pick a template file
    template_file = random.choice(self.heat_templates)
    template_data = self.get_file_contents(template_file)

    # params:
    if '1vm' in template_file:
        params['instance1_name'] = '%s-server-1' % (stack_name)
    elif '2vm' in template_file:
        params['instance1_name'] = '%s-server-1' % (stack_name)
        params['instance2_name'] = '%s-server-2' % (stack_name)

    # disable rollback
    if self.one_in_ten():
        disable_rollback=False

    # create the stack
    response = heat_base.create_stack(self,
                                      stack_name=stack_name,
                                      template=template_data,
                                      params=params,
                                      disable_rollback=disable_rollback,
                                      timeout_mins=timeout_mins)
    return response, stack_name


def update_stack(self):
    params = {}
    disable_rollback=True

    # get stack_name, stack_id
    stack_name, stack_id = heat_base.get_stack_name_and_id(self)

    # generate timeout
    timeout_mins = 30 # general default / maybe leave None(?)
    if self.one_in_ten():
        timeout_mins = random.choice([0,0,0,1,1,5,5,10,10,10,15,20,100,-1,'zebra golfcart tango',10000000000000000, .5])

    # pick a template file
    template_file = random.choice(self.heat_templates)
    template_data = self.get_file_contents(template_file)

    # params:
    if self.one_in_ten():
        if '1vm' in template_file:
            params['instance1_name'] = '%s-newname-1' % (stack_name)
        elif '2vm' in template_file:
            params['instance1_name'] = '%s-newname-1' % (stack_name)
            params['instance2_name'] = '%s-newname-2' % (stack_name)
    else:
        if '1vm' in template_file:
            params['instance1_name'] = '%s-server-1' % (stack_name)
        elif '2vm' in template_file:
            params['instance1_name'] = '%s-server-1' % (stack_name)
            params['instance2_name'] = '%s-server-2' % (stack_name)

    if self.one_in_five():
        params['flavor'] = random.choice(self.flavor_list)
    
    # disable rollback
    if self.one_in_ten():
        disable_rollback=False
    # set disable_rollback = False for testing
    disable_rollback=False

    # create the stack
    response = heat_base.update_stack(self,
                                      template=template_data,
                                      params=params,
                                      disable_rollback=disable_rollback,
                                      timeout_mins=timeout_mins)
    return response



def churn_stack_pool(self):
    """ This function is intended to do what it says - keep a create
        and delete cycle of stacks going.
        It is also intended as a chaos generator during heat tests
        stacks can be expected to randomly be deleted during operations

    """
 
    response = heat_base.list_stacks(self)
    stacks = json.loads(response.content)['stacks']
    if len(stacks) < self.min_stack_count:
        create_stack(self)
    elif len(stacks) >= self.max_stack_count:
        heat_base.delete_stack(self)

