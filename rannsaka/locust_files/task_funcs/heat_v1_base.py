import os
import json
import random
import string
import uuid

import nova_v2_base


def heat_request(self,
                 url_detail,
                 request_type='get',
                 request_name=None,
                 data=None,
                 locust_name=None):
    url = self.get_endpoint('orchestration')
    if url_detail:
        url = os.path.join(url, url_detail)
    headers = {'X-Auth-Project-Id': self.keystone_tenant,
               'X-Auth-Token': self.auth_token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    if data:
        response = getattr(self.client, request_type)(url,
                                                      headers=headers,
                                                      data=json.dumps(data),
                                                      name=locust_name)
    else:
        response = getattr(self.client, request_type)(url,
                                                      headers=headers,
                                                      name=locust_name)
    self.output(url)
    self.output("Response status code: %s" % response.status_code)
    self.output("Response content: %s" % response.content)
    return response


def get_stack_id(self):
    """ Return a random stack from currently
        available stacks
    """

    response = heat_request(self, 'stacks', 'get')
    stack_list = json.loads(response.content)['stacks']
    stack_id = random.choice([i['id'] for i in stack_list])
    return stack_id


def get_stack_name(self):
    response = heat_request(self, 'stacks', 'get')
    stack_list = json.loads(response.content)['stacks']
    stack_name = random.choice([i['stack_name'] for i in stack_list])
    return stack_name


def get_stack_name_and_id(self):
    # :/
    response = heat_request(self, 'stacks', 'get')
    stack_list = json.loads(response.content)['stacks']
    stack_choice = random.choice(stack_list)
    stack_name = stack_choice['stack_name']
    stack_id = stack_choice['id']
    return stack_name, stack_id


def get_snapshot_id(self, stack_id=None):
    """ Return a random snapshot from currently
        available snapshots
    """

    stack_name, stack_id = get_stack_name_and_id(self)
    url_path = 'stacks/%s/%s/snapshots' % (stack_name, stack_id)
    response = heat_request(self, url_path, 'get', locust_name='stacks/[name]/[id]/snapshots')
    snapshot_list = json.loads(response.content)['snapshots']
    snapshot_id = random.choice([i['id'] for i in snapshot_list])
    return snapshot_id, stack_name, stack_id


def list_stacks(self):
    return heat_request(self,
                       'stacks',
                       'get',
                       'heat_list_stacks')


def find_stack(self, stack_name=None):
    if not stack_name:
        stack_name = get_stack_name(self)
    return heat_request(self,
                       'stacks/%s' % stack_name,
                       'get',
                       'heat_find_stack',
                       locust_name='stacks/[name]')


def list_stack_detail(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                         'stacks/%s/%s' % (stack_name, stack_id),
                         'get',
                         'heat_list_stack_detail',
                         locust_name='stacks/[name]/[id]')


def list_resource_types(self):
    return heat_request(self,
                       'resource_types',
                       'get',
                       'heat_list_resource_types')


def list_snapshots(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       'stacks/%s/%s/snapshots' % (stack_name, stack_id),
                       'get',
                       'heat_list_snapshots',
                       locust_name='stacks/[name]/[id]/snapshots')


def list_snapshot_detail(self, snapshot_id=None):
    if not snapshot_id:
        snapshot_id, stack_name, stack_id = get_snapshot_id(self)
    return heat_request(self,
                       'stacks/%s/%s/snapshots/%s' % (stack_name, stack_id, snapshot_id),
                       'get',
                       'heat_list_snapshot_detail',
                       locust_name='stacks/[name]/[id]/snapshots/[snap_id]')


def find_stack_resources(self, stack_name=None):
    if not stack_name:
        stack_name = get_stack_name(self)
    return heat_request(self,
                       'stacks/%s/resources' % stack_name,
                       'get',
                       'heat_find_stack_resources',
                       locust_name='stacks/[name]/resources')


def list_stack_resources(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       'stacks/%s/%s/resources' % (stack_name, stack_id),
                       'get',
                       'heat_list_stack_resources',
                       locust_name='stacks/[name]/[id]/resources')


def find_stack_events(self, stack_name=None):
    if not stack_name:
        stack_name = get_stack_name(self)
    return heat_request(self,
                       'stacks/%s/events' % stack_name,
                       'get',
                       'heat_find_stack_events',
                       locust_name='stacks/[name]/events')


def list_stack_events(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       'stacks/%s/%s/events' % (stack_name, stack_id),
                       'get',
                       'heat_list_stack_events',
                       locust_name='stacks/[name]/[id]/events')


def get_stack_template(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    return heat_request(self,
                       'stacks/%s/%s/template' % (stack_name, stack_id),
                       'get',
                       'heat_get_stack_template',
                       locust_name='stacks/[name]/[id]/template')


def suspend_stack(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    data = {"suspend":None}
    return heat_request(self,
                       'stacks/%s/%s/actions' % (stack_name, stack_id),
                       'post',
                       'heat_suspend_stack',
                       data,
                       locust_name='stacks/[name]/[id]/[suspend_stack]')


def resume_stack(self, stack_name=None, stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    data = {"resume":None}
    return heat_request(self,
                       'stacks/%s/%s/actions' % (stack_name, stack_id),
                       'post',
                       'heat_resume_stack',
                       data,
                       locust_name='stacks/[name]/[id]/[resume_stack]')


def create_snapshot(self,
                    stack_name=None,
                    stack_id=None,
                    name=None,
                    force=False,
                    description=None):
    # TODO: don't set name unless passed as param
    if not name:
        name = "stack-snapshot-%s" % uuid.uuid4()
    data = {  "name": name,
           } 
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    response = heat_request(self,
                           'stacks/%s/%s/snapshots' %(stack_name, stack_id),
                            'post',
                            'heat_create_snapshot',
                            data,
                            locust_name='stacks/[name]/[id]/snapshots')
    return response


def delete_snapshot(self,
                  stack_name=None,
                  stack_id=None,
                  snapshot_id=None,
                  force=False,
                  description=None):
    if stack_name:
       snapshot_id = get_snapshot_id(stack_name=stack_name)
    if not snapshot_id:
        snapshot_id, stack_name, stack_id = get_snapshot_id(self) 
    response = heat_request(self,
                           'stacks/%s/%s/snapshots/%s' %(stack_name, stack_id, snapshot_id),
                           'delete',
                           'heat_delete_snapshot',
                           locust_name='stacks/[name]/[id]/snapshots/[delete_snapshot]')
    return response


def restore_snapshot(self,
                  stack_name=None,
                  stack_id=None,
                  snapshot_id=None,
                  force=False,
                  description=None):
    if stack_name:
       snapshot_id = get_snapshot_id(self, stack_name=stack_name)
    if not snapshot_id:
        snapshot_id, stack_name, stack_id = get_snapshot_id(self)
    response = heat_request(self,
                           'stacks/%s/%s/snapshots/%s/restore' %(stack_name, stack_id, snapshot_id),
                           'post',
                           'heat_restore_snapshot',
                           locust_name='stacks/[name]/[id]/snapshots/[restore_snapshot]')
    return response



def abandon_stack(self,
                 stack_name=None,
                 stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    response = heat_request(self,
                            'stacks/%s/%s/abandon' % (stack_name, stack_id),
                            'delete',
                            'heat_abandon_stack',
                            locust_name='stacks/[name]/[id]/abandon')
    return response


def adopt_stack(self,
               stack_name=None,
               template=None,
               template_url=None,
               timeout_mins=None,
               adopt_stack_data=None):
    if not stack_name:
        # generate one
        stack_name = 'test-stack-%s-%s' %(self.id, self.stack_count)
        self.stack_count += 1
    # TODO: generate other params if needed
    data = {'stack_name': stack_name,
            'template_url': template_url,
            'timeout_mins': timeout_mins,
            'adopt_stack_data': adopt_stack_data}
    if template:
        data['template'] = template
    response = heat_request(self,
                           'stacks',
                           'post',
                           'heat_adopt_stack',
                           data,
                           locust_name='stacks/[adopt_stack]')
    return response


def create_stack(self,
                 stack_name=None,
                 template=None,
                 template_url=None,
                 timeout_mins=None,
                 disable_rollback=True,
                 params=None):
    if not stack_name:
        # generate one
        stack_name = 'test-stack-%s-%s' %(self.id, self.stack_count)
        self.stack_count += 1
    # TODO: generate other params if needed
    data = {'stack_name': stack_name,
            'template_url': template_url,
            'timeout_mins': timeout_mins,
            'parameters' : params,
            'disable_rollback': disable_rollback}
    if template:
        data['template'] = template
    response = heat_request(self,
                           'stacks',
                           'post',
                           'heat_create_stack',
                           data,
                           locust_name='stacks/[create_stack]')
    return response


def delete_stack(self,
                 stack_name=None,
                 stack_id=None):
    if not stack_name:
        stack_name, stack_id = get_stack_name_and_id(self)
    response = heat_request(self,
                            'stacks/%s/%s' % (stack_name, stack_id),
                            'delete',
                            'heat_delete_stack',
                            locust_name='stacks/[name]/[id]')


def update_stack(self,
                 stack_name=None,
                 stack_id=None,
                 template=None,
                 template_url=None,
                 timeout_mins=None,
                 disable_rollback=True,
                 params=None):
    if not stack_name:
        # get one
        stack_name, stack_id = get_stack_name_and_id(self)
    # TODO: generate other params if needed
    data = {'stack_name': stack_name,
            'template_url': template_url,
            'timeout_mins': timeout_mins,
            'parameters' : params,
            'disable_rollback': disable_rollback}
    if template:
        data['template'] = template
    response = heat_request(self,
                           'stacks/%s/%s' % (stack_name, stack_id),
                           'put',
                           'heat_update_stack',
                           data,
                           locust_name='stacks/[stack_name]/[stack_id]/[update_stack]')
    return response

