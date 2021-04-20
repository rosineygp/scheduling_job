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
    assert(d.hour == 1)
    assert(d.minute == 0)
    assert(d.second == 0)

    d = scheduler.str_natural_to_time('2 horas')
    assert(d.hour == 2)
    assert(d.minute == 0)
    assert(d.second == 0)

    d = scheduler.str_natural_to_time('4 horas e 10 minutos')
    assert(d.hour == 4)
    assert(d.minute == 10)
    assert(d.second == 0)

    d = scheduler.str_natural_to_time('6 horas, 20 minutos e 35 segundos')
    assert(d.hour == 6)
    assert(d.minute == 20)
    assert(d.second == 35)

    d = scheduler.str_natural_to_time('1 hora, 20 minutos e 35 segundos')
    assert(d.hour == 1)
    assert(d.minute == 20)
    assert(d.second == 35)


if __name__ == "__main__":
    unittest.main()
