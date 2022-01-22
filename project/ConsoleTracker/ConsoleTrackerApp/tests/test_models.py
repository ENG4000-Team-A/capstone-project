import datetime
import sys
import pytz

from django.test import TestCase
from django.utils import timezone
from ..models import TimeStamp, Machine, User, User_uses_machine

'''
    Boundary Value Testing With Single Fault Assumptions
    
    +---------+---------+--------------------+---------+--------------------+--------------------+
    |         | Minimum | Just Above Minimum | Nominal | Maximum            | Just Below Maximum |
    +---------+---------+--------------------+---------+--------------------+--------------------+
    | hours   | 0       | 1                  | 50      | Integer MAX        | Integer MAX - 1    |
    +---------+---------+--------------------+---------+--------------------+--------------------+
    | minutes | 0       | 1                  | 30      | 60                 | 59                 |
    +---------+---------+--------------------+---------+--------------------+--------------------+
    | seconds | 0       | 1                  | 30      | 60                 | 59                 |
    +---------+---------+--------------------+---------+--------------------+--------------------+
'''


class TestTimeStamp(TestCase):
    def setUp(self):
        TimeStamp.objects.create(hours=0, minutes=30, seconds=30)
        TimeStamp.objects.create(hours=1, minutes=30, seconds=30)
        TimeStamp.objects.create(hours=50, minutes=30, seconds=30)
        TimeStamp.objects.create(hours=sys.maxsize, minutes=30, seconds=30)
        TimeStamp.objects.create(hours=sys.maxsize - 1, minutes=30, seconds=30)
        TimeStamp.objects.create(hours=50, minutes=0, seconds=30)
        TimeStamp.objects.create(hours=50, minutes=1, seconds=30)
        TimeStamp.objects.create(hours=50, minutes=30, seconds=30)
        TimeStamp.objects.create(hours=50, minutes=60, seconds=30)
        TimeStamp.objects.create(hours=50, minutes=59, seconds=30)
        TimeStamp.objects.create(hours=50, minutes=30, seconds=0)
        TimeStamp.objects.create(hours=50, minutes=30, seconds=1)
        TimeStamp.objects.create(hours=50, minutes=30, seconds=60)
        TimeStamp.objects.create(hours=50, minutes=30, seconds=59)

    def test_boundary_values(self):
        hours = [0, 1, 50, sys.maxsize, sys.maxsize - 1, 50, 50, 50, 50, 50, 50, 50, 50, 50]
        minutes = [30, 30, 30, 30, 30, 0, 1, 30, 60, 59, 30, 30, 30, 30]
        seconds = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 0, 1, 60, 59]
        timestamps = TimeStamp.objects.all()
        for count, timestamp in enumerate(timestamps):
            self.assertEqual(timestamp.hours, hours[count])
            self.assertEqual(timestamp.minutes, minutes[count])
            self.assertEqual(timestamp.seconds, seconds[count])

        # Reset Objects
        TimeStamp.objects.all().delete()
        self.assertEqual(TimeStamp.objects.count(), 0)

        # Assert Default Values
        obj = TimeStamp.objects.create()
        self.assertEqual(obj.hours, 0)
        self.assertEqual(obj.minutes, 0)
        self.assertEqual(obj.seconds, 0)


'''
    Equivalence Class Testing With Weak Normal ECT
    
    name = {"", "John", "Chris"}
    active = {True, False}
    ip = {"127.0.0.1", "192.168.1"}
    
    +--------+--------+--------+-------------+
    |        | name   | active | ip          |
    +--------+--------+--------+-------------+
    | Case 1 | ""     | True   | "127.0.0.1" |
    +--------+--------+--------+-------------+
    | Case 2 | "John" | False  | "192.168.1" |
    +--------+--------+--------+-------------+
    | Case 3 | "Chris"| True   | "132.168.1" |
    +--------+--------+--------+-------------+
'''


class TestMachine(TestCase):
    def setUp(self):
        Machine.objects.create(name="", active=True, ip="127.0.0.1")
        Machine.objects.create(name="John", active=False, ip="192.168.1")
        Machine.objects.create(name="Chris", active=True, ip="132.168.1")

    def test_equivalence_values(self):
        names = ["", "John", "Chris"]
        actives = [True, False, True]
        ips = ["127.0.0.1", "192.168.1", "132.168.1"]

        machines = Machine.objects.all()
        for count, machine in enumerate(machines):
            self.assertEqual(machine.name, names[count])
            self.assertEqual(machine.active, actives[count])
            self.assertEqual(machine.ip, ips[count])

        # Reset Objects
        Machine.objects.all().delete()
        self.assertEqual(Machine.objects.count(), 0)

        # Assert Default Values
        obj = Machine.objects.create()
        self.assertEqual(obj.name, "")
        self.assertEqual(obj.active, False)
        self.assertEqual(obj.ip, "127.0.0.1")


'''
    Boundary Value Testing With Single Fault Assumptions

    +---------+--------------+--------------------+---------+--------------------+--------------------+
    |         | Minimum      | Just Above Minimum | Nominal | Maximum            | Just Below Maximum |
    +---------+--------------+--------------------+---------+--------------------+--------------------+
    | time    | 0            | 1                  | 5000    | Integer MAX        | Integer MAX - 1    |
    +---------+--------------+--------------------+---------+--------------------+--------------------+
'''


class TestUser(TestCase):
    def setUp(self):
        User.objects.create(username="John1", time=0, first_name="John",
                            last_name="Doe", phone_number="123-456-7890")
        User.objects.create(username="John2", time=1, first_name="John",
                            last_name="Doe", phone_number="123-456-7890")
        User.objects.create(username="John3", time=5000, first_name="John",
                            last_name="Doe", phone_number="123-456-7890")
        User.objects.create(username="John4", time=sys.maxsize, first_name="John",
                            last_name="Doe", phone_number="123-456-7890")
        User.objects.create(username="John5", time=sys.maxsize - 1, first_name="John",
                            last_name="Doe", phone_number="123-456-7890")

    def test_equivalence_values(self):
        usernames = ["John1", "John2", "John3", "John4", "John5"]
        first_names = ["John", "John", "John", "John", "John"]
        last_names = ["Doe", "Doe", "Doe", "Doe", "Doe"]
        times = [0, 1, 5000, sys.maxsize, sys.maxsize - 1]
        phone_numbers = ["123-456-7890", "123-456-7890", "123-456-7890", "123-456-7890", "123-456-7890"]

        users = User.objects.all()
        for count, user in enumerate(users):
            self.assertEqual(user.username, usernames[count])
            self.assertEqual(user.first_name, first_names[count])
            self.assertEqual(user.last_name, last_names[count])
            self.assertEqual(user.time, times[count])
            self.assertEqual(user.phone_number, phone_numbers[count])


        # Reset Objects
        User.objects.all().delete()
        self.assertEqual(User.objects.count(), 0)

        # Assert Default Values
        obj = User.objects.create()
        self.assertEqual(obj.username, "")
        self.assertEqual(obj.first_name, "")
        self.assertEqual(obj.last_name, "")
        self.assertEqual(obj.time, 0)
        self.assertEqual(obj.phone_number, "")


'''
    Equivalence Class Testing With Weak Normal ECT For Readonly Values
    
    start_time = {Time Now, datetime(2011, 8, 15, 8, 15, 12, 0, UTC)}
    end_time = {Time Now + User Time, datetime(2011, 8, 15, 8, 15, 12, 0, UTC) + User Time}
    expired = {True, False}

    +--------+------------------------------------------+----------------------------------------------------+---------+
    |        | start_time                               | end_time                                           | expired |
    +--------+------------------------------------------+----------------------------------------------------+---------+
    | Case 1 | Time Now                                 | Time Now + User Time                               | True    |
    +--------+------------------------------------------+----------------------------------------------------+---------+
    | Case 2 | datetime(2011, 8, 15, 8, 15, 12, 0, UTC) | datetime(2011, 8, 15, 8, 15, 12, 0, UTC)+User Time | False   |
    +--------+------------------------------------------+----------------------------------------------------+---------+
    | Case 3 | Time Now                                 | Time Now + User Time                               | True    |
    +--------+------------------------------------------+----------------------------------------------------+---------+
'''


class TestUserUsesMachine(TestCase):
    def setUp(self):
        now = datetime.datetime.now(pytz.UTC)

        machine1 = Machine.objects.create(name="Eric", active=True, ip="127.0.0.1")
        user1 = User.objects.create(username="John1", time=5000, first_name="John",
                                    last_name="Doe", phone_number="123-456-7890")
        User_uses_machine.objects.create(user=user1, machine=machine1, expired=True)

        machine2 = Machine.objects.create(name="Alex", active=True, ip="137.0.0.1")
        user2 = User.objects.create(username="John2", time=5000, first_name="John",
                                    last_name="Doe", phone_number="123-456-7890")
        User_uses_machine.objects.create(user=user2, machine=machine2,
                                         start_time=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC),
                                         expired=False)

        machine3 = Machine.objects.create(name="John", active=True, ip="117.0.0.1")
        user3 = User.objects.create(username="John3", time=5000, first_name="John",
                                    last_name="Doe", phone_number="123-456-7890")
        User_uses_machine.objects.create(user=user3, machine=machine3,
                                         end_time=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC),
                                         expired=True)

    def test_equivalence_values(self):
        now = datetime.datetime.now(pytz.UTC)
        set_time = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)
        user_time = + timezone.timedelta(seconds=5000)
        start_times = [now, set_time, now]
        end_times = [now + user_time, set_time + user_time, now + user_time]
        expireds = [True, False, True]

        User_uses_machines = User_uses_machine.objects.all()
        for count, user_uses_machine in enumerate(User_uses_machines):
            # Check if the diff between start times is less than 1 seconds because of delay
            self.assertTrue(abs(user_uses_machine.start_time - start_times[count]) < datetime.timedelta(seconds=1))
            self.assertTrue(abs(user_uses_machine.end_time - end_times[count]) < datetime.timedelta(days=1))
            self.assertEqual(user_uses_machine.expired, expireds[count])

    def test_relationships(self):
        # Check if mappings correlate to correct reference keys
        machine_ips = ["127.0.0.1", "137.0.0.1", "117.0.0.1"]
        user_names = ["John1", "John2", "John3"]

        User_uses_machines = User_uses_machine.objects.all()
        for count, user_uses_machine in enumerate(User_uses_machines):
            self.assertEqual(user_uses_machine.machine.ip, machine_ips[count])
            self.assertEqual(user_uses_machine.user.username, user_names[count])

        # Reset Objects
        User_uses_machine.objects.all().delete()
        self.assertEqual(User_uses_machine.objects.count(), 0)
