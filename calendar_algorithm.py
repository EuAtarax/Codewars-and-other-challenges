"""
This script finds possible times in a day, during which a meeting can be held.
It uses 2 calendars with set meetings as input and will try to find some timepoints,
which could be used for a potential meeting.
Further, there are daily boundaries, after which no meeting shall be scheduled and a
meeting length.
The input will be sorted and within the set boundaries.

Input example:
[['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
['9:00', '20:00']
[['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
['10:00', '18:30']
30

Output example:
[[11:30', '12:00'], ['15:00', '16:00'], ['18:00', '18:30']]


"""

ca1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
bo1 = ['8:00', '20:00']
ca2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
bo2 = ['7:00', '18:30']
length = 30


def find_meeting(c1, b1, c2, b2, l):
    # do the magic of finding all possible dates

    # merge both lists in a magical way, where meetings are merged and breaks stay available
    print('start to merge')
    out = []
    booked_times = []
    p1 = 0
    p2 = 0

    while p1 + p2 < len(c1) + len(c2):
        if p1 == len(c1):
            print('hit end of p1')
            booked_times.extend(c2[p2:])
            break

        if p2 == len(c2):
            print('hit end of p2')
            booked_times.extend(c1[p1:])
            break

        if cmp_times(c1[p1][0], c2[p2][0]) == -1:  # p1 < p2
            booked_times.append(c1[p1])
            p1 += 1
        else:  # p1 > p2
            booked_times.append(c2[p2])
            p2 += 1

    print('done with the merging')
    print(booked_times)

    i = 0
    while i < len(booked_times) - 1:
        print(f'i = {i}')
        end1 = booked_times[i][1]
        start2 = booked_times[i + 1][0]

        # if end > start, pop start2 & compare end 1:end2; pop if necessary
        if cmp_times(end1, start2) == 1:
            booked_times[i + 1].pop(0)
            start2 = booked_times[i + 1][0]
            if cmp_times(end1, start2) == 1:
                booked_times[i][1] = start2
                del booked_times[i + 1]
            else:
                booked_times[i][1] = start2
                del booked_times[i + 1]

        # if the start2 should be greater than end1, make end1 = end2; pop second element completely
        else:
            # check length of break in between and append if long enough
            e1, s2 = convert_time(booked_times[i][1], booked_times[i + 1][0])
            if s2 - e1 >= l:
                out.append([end1, start2])
                i += 1

            else:
                i += 1

    # remove too early/late meeting possibilities
    # first, create new boundary
    final_b = []
    if cmp_times(b1[0], b2[0]) == -1:
        final_b.append(b2[0])
    else:
        final_b.append(b1[0])

    if cmp_times(b1[1], b2[1]) == 1:
        final_b.append(b2[1])
    else:
        final_b.append(b1[1])

    # now check the boundaries for possible meetings
    if cmp_times(final_b[0], booked_times[0][0]) == -1:
        out.insert(0, [final_b[0], booked_times[0][0]])
    if cmp_times(final_b[1], booked_times[-1][1]) == 1:
        out.append([booked_times[-1][1], final_b[1]])

    print('find_meeting - finished')
    return out


def cmp_times(t1, t2):
    h1, m1 = t1.split(":")
    h2, m2 = t2.split(":")

    time1 = int(h1) * 60 + int(m1)
    time2 = int(h2) * 60 + int(m2)

    if time1 >= time2:
        return 1
    elif time1 < time2:
        return -1


def convert_time(t1, t2):
    # this function takes in a list of times in strings and outputs the same list with numbers.
    # input is a list of tuples containing start/end time of a meeting
    h1, m1 = t1.split(":")
    h2, m2 = t2.split(":")

    time1 = int(h1) * 60 + int(m1)
    time2 = int(h2) * 60 + int(m2)

    return time1, time2


# run the show
meets = find_meeting(ca1, bo1, ca2, bo2, length)
print(meets)
print('done')
