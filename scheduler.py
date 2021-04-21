import json
from datetime import datetime, timedelta
import re
import pprint

pp = pprint.PrettyPrinter()


def str_to_time(strtime):
  return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')


# 2 horas e 55 minutos
def str_natural_to_time(str):
  hours = 0
  minutes = 0
  seconds = 0

  tokens = str.split()

  for i in range(len(tokens)):
    try:
      n = int(tokens[i])

      time_str = tokens[i + 1]
      if re.search('^hora(s|)(,|)$', time_str):
        hours = n
      elif re.search('^minuto(s|)(,|)$', time_str):
        minutes = n
      elif re.search('^segundo(s|)(,|)$', time_str):
        seconds = n
    except:
      pass

  # return datetime.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")
  return {
      'hours': hours,
      'minutes': minutes,
      'seconds': seconds,
      'datetime': datetime.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")
  }


ini = str_to_time("2019-11-10 09:00:00")
end = str_to_time("2019-11-11 12:00:00")


def scheduler_windows_filter(item):
  if item['Data Máxima de conclusão'] >= ini and item['Data Máxima de conclusão'] <= end:
    return True

  return False


def sum_until_max(slice, max):

  hours = 0
  minutes = 0
  seconds = 0

  result = []

  for i, item in enumerate(slice):
    hours += item['Tempo estimado']['hours']
    minutes += item['Tempo estimado']['minutes']
    seconds += item['Tempo estimado']['seconds']

    t = datetime.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")

    result.append(item['ID'])
    if t >= max:
      return list(result)

  return result


if __name__ == "__main__":
  with open('jobs.json') as json_file:
    data = json.load(json_file)

  # fix data
  for i in data:
    i['Data Máxima de conclusão'] = str_to_time(i['Data Máxima de conclusão'])
    i['Tempo estimado'] = str_natural_to_time(i['Tempo estimado'])

  data = sorted(data, key=lambda k: k['Data Máxima de conclusão'])

  max_time = str_natural_to_time('8 horas')
  filtered = list(filter(scheduler_windows_filter, data))

  out = []
  i = 0
  while i < len(filtered):
    item = filtered[i]
    if item['Tempo estimado']['datetime'] > max_time['datetime']:
      print(f"o job '{item['ID']}'  não pode ser processado > janela diaria!")
      i += 1
    elif item['Tempo estimado']['datetime'] == max_time['datetime']:
      out.append([item['ID']])
      i += 1
    else:
      items = sum_until_max(filtered[i:], max_time['datetime'])
      out.append(items)
      i += len(items)

  pp.pprint(out)
