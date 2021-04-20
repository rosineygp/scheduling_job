import json
from datetime import datetime


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
      if time_str == 'horas':
        hours = n
      elif time_str == 'minutos':
        minutes = n
      elif time_str == 'segundos':
        seconds = n
    except:
      pass

  return datetime.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")


with open('jobs.json') as json_file:
  data = json.load(json_file)


# fix data
for i in data:
  i['Data Máxima de conclusão'] = str_to_time(i['Data Máxima de conclusão'])
  i['Tempo estimado'] = str_natural_to_time(i['Tempo estimado'])

print(data)
