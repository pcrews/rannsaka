import os

def nova_get_request(self, url_detail):
    url = self.get_endpoint('compute')
    if url_detail:
        url = os.path.join(url, url_detail)
    headers = {'X-Auth-Project-Id': self.keystone_tenant,
               'X-Auth-Token': self.auth_token}
    response = self.client.get(url, headers=headers)
    self.output(url)
    self.output("Response status code: %s" % response.status_code)
    #self.output("Response content: %s" % response.content)

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
