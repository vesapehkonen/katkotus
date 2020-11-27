import argparse
import datetime


def print_time(line_num, start, end, td, notes=''):
    h = td.seconds//3600
    m = (td.seconds//60)%60
    s = td.seconds - (td.seconds//60) * 60  # delta seconds includes also minutes, so they are needed to decrease from seconds
    f = int(td.microseconds * 25 / 1000000)
    print('{}\t{}\t{}\t{:02d}:{:02d}:{:02d}:{:02d} {}'.format(line_num, start, end, h, m, s, f, notes))

def parse_line(line_num, start, end, notes):
    [h1, m1, s1, f1] = start.split(':')
    [h2, m2, s2, f2] = end.split(':')
    f1 = int(f1) * 1000 / 25 # frames to milliseconds
    f2 = int(f2) * 1000 / 25 # frames to milliseconds

    td1 = datetime.timedelta(hours=int(h1), minutes=int(m1), seconds=int(s1), milliseconds=f1)
    td2 = datetime.timedelta(hours=int(h2), minutes=int(m2), seconds=int(s2), milliseconds=f2)

    if td1 > td2:
        raise ValueError('The start time is bigger than end the time: {} {}'.format(start, end))
    
    td3 = td2 - td1

    print_time(line_num, start, end, td3, notes)
    return td3

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', type=str, help='inputfile')
    args = parser.parse_args()
    inputfile = args.inputfile

    overall_time = datetime.timedelta(seconds=0)
    try:
        with open(inputfile, encoding='utf-8') as f:
            lines = f.readlines()
    except:
        with open(inputfile, encoding='utf-16') as f:
            lines = f.readlines()
        
    for line in lines:
        columns = line.split()
        if len(columns) >= 3:
            line_number = columns[0]
            start = columns[1]
            end = columns[2]
            #if len(columns) > 3:
            notes = ''
            for column in columns[3:]:
                notes = notes + column + ' '
            overall_time += parse_line(line_number, start, end, notes)

    print_time('', '', '', overall_time)
