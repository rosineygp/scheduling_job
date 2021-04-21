import json
from datetime import datetime, timedelta
import re


def str_to_time(strtime):
    """
    Convert str('%Y-%m-%d %H:%M:%S') to datetime.

    Parameters:
    strtime (str): date and time

    Returns:
    datetime: Object datetime
    """
    return datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')


def str_natural_to_time(str):
    """
    Convert natural brazilian time string to dict.

    eg. (2 horas e 30 minutos, 1 hora, 8 horas,...)

    Parameters:
    str (str): Brazilian natural hours

    Returns:
    dict:
      int: hours
      int: minutes
      int: seconds
      datetime: Object datetime
    """
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

    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'datetime': datetime.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")
    }


def make_window_filter(ini, end):
    """
    Set window parameters for window_filter function.

    Parameters:
    ini (datetime): the beginning of schedule window
    end (datetime): the end of schedule window

    Returns:
    window_filter (lambda): Parametrized sort function
    """

    def window_filter(item):
        """
        Filter jobs between ini and end execution window.

        Parameters:
        item(dict): single job dict

        Returns:
        Boolean: True if the job is in window execution interval, otherwise false.
        """
        if item['Data Máxima de conclusão'] >= ini and item['Data Máxima de conclusão'] <= end:
            return True

        return False
    return window_filter


def sum_until_max(slice, max):
    """
    Sum slice of jobs and break if is lt max

    Parameters:
    slice (array): List of jobs
    max (dict): Max windows execution

    Returns:
    array: Array with jobs ids (daily window)
    """
    hours = 0
    minutes = 0
    seconds = 0

    result = []

    for i, item in enumerate(slice):
        hours += item['Tempo estimado']['hours']
        minutes += item['Tempo estimado']['minutes']
        seconds += item['Tempo estimado']['seconds']

        t = datetime.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")

        if t <= max:
            result.append(item['ID'])
        else:
            break

    return result


if __name__ == "__main__":
    with open('jobs.json') as json_file:
        data = json.load(json_file)

    # normalize data
    for i in data:
        i['Data Máxima de conclusão'] = str_to_time(
            i['Data Máxima de conclusão'])
        i['Tempo estimado'] = str_natural_to_time(i['Tempo estimado'])

    # sort data by 'Data Máxima de conclusão'
    data = sorted(data, key=lambda k: k['Data Máxima de conclusão'])

    # generate initial max_time like docs
    max_time = str_natural_to_time('8 horas')

    # remove jobs outside execution window
    ini = str_to_time("2019-11-10 09:00:00")
    end = str_to_time("2019-11-11 12:00:00")

    wf = make_window_filter(ini, end)
    filtered = list(filter(wf, data))

    out = []
    i = 0
    while i < len(filtered):
        item = filtered[i]
        if item['Tempo estimado']['datetime'] > max_time['datetime']:
            print(
                f"o job '{item['ID']}'  não pode ser processado > janela diaria!")
            i += 1
        elif item['Tempo estimado']['datetime'] == max_time['datetime']:
            out.append([item['ID']])
            i += 1
        else:
            items = sum_until_max(filtered[i:], max_time['datetime'])
            out.append(items)
            i += len(items)

    print(out)
