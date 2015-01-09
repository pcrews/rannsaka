import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

import task_sets.basic_get as basic_get 

class NovaBasicTestUser(HttpLocust):
    task_set = basic_get.basicGet 
    min_wait=100
    max_wait=1000
