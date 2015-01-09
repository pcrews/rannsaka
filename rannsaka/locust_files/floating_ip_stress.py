import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

import task_sets.floating_ip_stress as vip_test 

class VipStressUser(HttpLocust):
    task_set = vip_test.VipStress 
    min_wait=500
    max_wait=3000
