import os
import json
import string
import random

def nova_get_request(self, url_detail):
    url = self.get_endpoint('compute')
    if url_detail:
        url = os.path.join(url, url_detail)
    headers = {'X-Auth-Project-Id': self.keystone_tenant,
               'X-Auth-Token': self.auth_token}
    response = self.client.get(url, headers=headers)
    self.output(url)
    self.output("Response status code: %s" % response.status_code)
    self.output("Response content: %s" % response.content)
    return response

def nova_post_request(self, url_detail, data):
    url = self.get_endpoint('compute')
    if url_detail:
        url = os.path.join(url, url_detail)
    headers = {'X-Auth-Project-Id': self.keystone_tenant,
               'X-Auth-Token': self.auth_token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    response = self.client.post(url,
                               headers=headers,
                               data=json.dumps(data))
    self.output(url)
    self.output("Response status code: %s" % response.status_code)
    self.output("Response content: %s" % response.content)
    return response

def nova_get_image_id(self):
    """ Return a random image from currently
        available images
    """

    response = nova_get_request(self, 'images')
    image_list = json.loads(response.content)['images']
    image_id = random.choice([i['id'] for i in image_list])
    return image_id

def nova_get_test_metadata(self):
    """ TODO - allow flag + image_id
        if received, then get actual
        metadata (?)
 
    """
    key_counts = [1,1,1,1,1,
                  3,3,3,3,
                  5,5,5,
                  10,
                  100]
    value_pop = string.ascii_uppercase + string.ascii_lowercase + string.digits
    key_count = random.choice(key_counts)
    metadata = {}
    for i in range(key_count):
        key_name = 'key%s' % i
        #value_len = random.randint(0,199)
        value_len = random.choice(key_counts)
        value = ''.join(random.choice(value_pop) for i in range(value_len))
        metadata[key_name] = value
    print metadata
    return metadata

def list_servers(self):
    nova_get_request(self, 'servers')

def list_servers_detail(self):
    nova_get_request(self, 'servers/detail')

def list_flavors(self):
    nova_get_request(self, 'flavors')

def list_flavors_detail(self):
    nova_get_request(self, 'flavors/detail')

def list_limits(self):
    nova_get_request(self, 'limits')

def list_images(self):
    nova_get_request(self, 'images')

def list_images_detail(self):
    nova_get_request(self, 'images/detail')

def list_image_detail(self, image_id=None):
    if not image_id:
        # get available images and randomly
        # choose one
        image_id = nova_get_image_id(self) 
    nova_get_request(self, 'images/%s' % image_id)

def list_image_metadata(self, image_id=None):
    if not image_id:
        image_id = nova_get_image_id(self)
    nova_get_request(self, 'images/%s/metadata' % image_id)

def update_image_metadata(self, image_id = None, metadata=None):
    if not image_id:
        image_id = nova_get_image_id(self)
    if not metadata:
        metadata = nova_get_test_metadata(self)
    data = {"metadata":metadata}
    nova_post_request(self,
                      'images/%s/metadata' % image_id,
                      data)
