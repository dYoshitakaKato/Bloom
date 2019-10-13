import datetime

class Reservation():
    def __init__(self, string: str):
        strs = string.split(',')
        self.date = strs[0].replace('insertLabelTime(\'', '').replace('\'', '').strip()
        self.startTime = self.convert_time(strs[1].replace('parseFloat(\'', '').replace('\')', '').strip())
        self.endTime = self.convert_time(strs[2].replace('parseFloat(\'', '').replace('\')', '').strip())
        self.officeNumber = strs[3].strip().strip('\'')
        self.color = strs[4]
        self.drag = strs[5]
        self.title = strs[6]
        self.id = strs[7].strip(' ')
        self.periodNumber = strs[8]
        self.toolTip = strs[9]
        self.multipleWeekday = strs[10]
        self.reservationUpdateDate = strs[11]
        self.reservationAllDay = strs[12]
        self.reservationUser = strs[13]
        pass

    def convert_time(self, strTime: str):
        times = strTime.strip('  ').split('.')
        if len(times) == 1:
            return times[0] + ':00'
        float_time = float(times[1])
        time = str((float(times[1]) * 60)).replace('00.0', '')
        return (times[0] + ':' + time).replace(':3', ':30')

    def create_datetime(self, date: str, strTime: str):
        times = strTime.strip('  ').split('.')
        time = times[0] + ':00'
        if times[0] == '24':
            times[0] = '0'
            return datetime.datetime.strptime(date, '%Y/%m/%d') + datetime.timedelta(days=1)
        if len(times) == 1:
            time = times[0] + ':00'
            print(date + ' ' + time)
            return datetime.datetime.strptime(date + ' ' + time, '%Y/%m/%d %H:%M')
        if times[1] == '25':
            time = times[0] + ':15'
        if times[1] == '5':
            time = times[0] + ':30'
        if times[1] == '75':
            time = times[0] + ':45'
        print(date + ' ' + time)
        return datetime.datetime.strptime(date + ' ' + time, '%Y/%m/%d %H:%M')


