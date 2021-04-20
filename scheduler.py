import json
from datetime import datetime
import re
import pprint

pp = pprint.PrettyPrinter()

def str_to_time(strtime):
  return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')


# 2 horas e 55 minutos
def str_natural_to_time(str):
  hours = "00"
  minutes = "00"
  seconds = "00"

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

  return datetime.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")


if __name__ == "__main__":
  with open('jobs.json') as json_file:
    data = json.load(json_file)


  # fix data
  for i in data:
    i['Data Máxima de conclusão'] = str_to_time(i['Data Máxima de conclusão'])
    i['Tempo estimado'] = str_natural_to_time(i['Tempo estimado'])

  data = sorted(data, key=lambda k: k['Data Máxima de conclusão'])
  pp.pprint(data)

  # pp.pprint(sorted(data, key=lambda k: k['Data Máxima de conclusão']))