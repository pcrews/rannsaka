import commands
import time

import MySQLdb

from locust import Locust, events, task, TaskSet

def show_tables(self):
            print "Running show_tables..."
            print self.client.query("SHOW TABLES IN mysql", name="SHOW TABLES")

def mysql_user(self):
            print "Running show users..."
            print self.client.query("SELECT * FROM mysql.user", name="SHOW USERS")

def city_select(self):
            print "City SELECT..."
            query = "SELECT * FROM City"
            name = "City SELECT"
            print "%s: %s" %(self.id, len(self.client.query(query, name)) )

def country_select(self):
            print "Country SELECT..."
            query = "SELECT * FROM Country"
            name = "Country SELECT"
            print "%s: %s" %(self.id, len(self.client.query(query, name)) )

def two_table_join(self):
            print "2 table JOIN..."
            query = "SELECT * FROM City, Country WHERE City.CountryCode=Country.Code"
            name = "two_table_join"
            print "%s: %s" %(self.id, len(self.client.query(query, name)) )

def three_table_join(self):
            print "3 table JOIN..."
            query = "SELECT * FROM City, Country, CountryLanguage WHERE City.CountryCode=Country.Code AND CountryLanguage.CountryCode=Country.Code"
            name = "three_table_join"
            print "%s: %s" %(self.id, len(self.client.query(query, name)) )


class MariadbClient():
    """
    Simple, sample XML RPC client implementation that wraps xmlrpclib.ServerProxy and 
    fires locust events on request_success and request_failure, so that all requests 
    gets tracked in locust's statistics.
    """
    def __init__(self):
        try:
            print 'Hello!'
        except Exception as e:
            print Exception, e

    def query(self, query, name):
            start_time = time.time()
            try:
                cmd = 'mysql -uroot world -e "%s"' %query 
                status, output = commands.getstatusoutput(cmd)
                print "%s\ncmd: %s\nstatus: %s\n\n%s" %('#'*80, cmd, status, '#'*80)
            except Exception as e:
                total_time = float((time.time() - start_time) * 1000)
                print Exception, e
                events.request_failure.fire(request_type="mariadb", name=name, response_time=total_time, exception=e)
                return None
            else:
                total_time = float((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="mariadb", name=name, response_time=total_time, response_length=0)
                # In this example, I've hardcoded response_length=0. If we would want the response length to be 
                # reported correctly in the statistics, we would probably need to hook in at a lower level
                return output 

class Task_set(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.id = str(self.locust).split('object at')[1].strip().replace('>','')

    tasks = {three_table_join: 10,
             two_table_join: 5,
             city_select: 3,
             country_select: 1
            }
        

class MariadbLocust(Locust):
    """
    This is the abstract Locust class which should be subclassed. It provides an XML-RPC client
    that can be used to make XML-RPC requests that will be tracked in Locust's statistics.
    """
    def __init__(self, *args, **kwargs):
        super(MariadbLocust, self).__init__(*args, **kwargs)
        self.client = MariadbClient()
        task_set = Task_set


class ApiUser(MariadbLocust):
    def __init__(self):
        super(ApiUser, self).__init__()
        self.host = "http://127.0.0.1:3306/"
        self.min_wait = 0 
        self.max_wait = 10 
    task_set = Task_set
