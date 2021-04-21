import unittest
from datetime import datetime

import scheduler


class TestScheduler(unittest.TestCase):
  def test_str_to_time(self):
    d = scheduler.str_to_time('2019-11-10 12:00:00')
    assert(d.year == 2019)
    assert(d.month == 11)
    assert(d.day == 10)
    assert(d.hour == 12)
    assert(d.minute == 0)
    assert(d.second == 0)

  def test_str_natural_to_time(self):
    d = scheduler.str_natural_to_time('1 hora')
    assert(d['hours'] == 1)
    assert(d['minutes'] == 0)
    assert(d['seconds'] == 0)
    assert(d['datetime'].hour == 1)
    assert(d['datetime'].minute == 0)
    assert(d['datetime'].second == 0)

    d = scheduler.str_natural_to_time('2 horas')
    assert(d['hours'] == 2)
    assert(d['minutes'] == 0)
    assert(d['seconds'] == 0)
    assert(d['datetime'].hour == 2)
    assert(d['datetime'].minute == 0)
    assert(d['datetime'].second == 0)

    d = scheduler.str_natural_to_time('4 horas e 10 minutos')
    assert(d['hours'] == 4)
    assert(d['minutes'] == 10)
    assert(d['seconds'] == 0)
    assert(d['datetime'].hour == 4)
    assert(d['datetime'].minute == 10)
    assert(d['datetime'].second == 0)

    d = scheduler.str_natural_to_time('6 horas, 20 minutos e 35 segundos')
    assert(d['hours'] == 6)
    assert(d['minutes'] == 20)
    assert(d['seconds'] == 35)
    assert(d['datetime'].hour == 6)
    assert(d['datetime'].minute == 20)
    assert(d['datetime'].second == 35)

    d = scheduler.str_natural_to_time('1 hora, 20 minutos e 35 segundos')
    assert(d['hours'] == 1)
    assert(d['minutes'] == 20)
    assert(d['seconds'] == 35)
    assert(d['datetime'].hour == 1)
    assert(d['datetime'].minute == 20)
    assert(d['datetime'].second == 35)


if __name__ == "__main__":
    unittest.main()
