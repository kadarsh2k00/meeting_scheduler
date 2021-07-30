### function to find the free slots of given employees
def find_free_time_slots(employee_ids, start_time, end_time):

# get all the slots of all employee_ids with given start and end time
    all_busy_slots = []
    for eid in employee_ids:
        for meeting in emp[eid]:
            if (meeting[0] < start_time and meeting[1] < start_time) or meeting[0] > end_time:
                continue
            all_busy_slots.append(meeting)
    all_busy_slots.sort()

# get the start time of first free slot between start and end time 
    length = len(all_busy_slots)
    get_start_time = None
    i = 0
    while i < length:
        if all_busy_slots[i][0] <= start_time:
            if get_start_time is None:
                get_start_time = all_busy_slots[i][1]
            else:
                get_start_time = max(get_start_time, all_busy_slots[i][1])
        else: break
        i += 1
    if get_start_time == None:
        get_start_time = start_time
    all_busy_slots = all_busy_slots[i:]

# get the end time of last free slot between start and end time    
    length = len(all_busy_slots)   
    get_end_time = None
    i = length-1
    while i >= 0:
        if all_busy_slots[i][1] >= end_time:
            if get_end_time is None:
                get_end_time = all_busy_slots[i][0]
            else:
                get_end_time = min(get_end_time, all_busy_slots[i][0])
        else: break
        i -= 1
    if get_end_time == None:
        get_end_time = end_time
    all_busy_slots = all_busy_slots[:i+1]


    length = len(all_busy_slots)
# if no busy slots between start and end time return whole slot
    if length == 0:
        return [(get_start_time, get_end_time)]

# get all the free slots from given busy slots between start and end time
    i = 0
    free_time = []
    while i < length:
        meeting = all_busy_slots[i]
        if get_start_time < meeting[0]:
            free_time.append((get_start_time, meeting[0]))
            get_start_time = meeting[1]
        elif get_start_time > meeting[0]:
            get_start_time = max(get_start_time, meeting[1])
        else:
            get_start_time = meeting[1]
        i += 1        
    if get_start_time < get_end_time:
        free_time.append((get_start_time, get_end_time))

# return the list of available free slots
    return free_time



### function to book the meeting
def bookMeeting(organizer_id, start_time, end_time):

# get all previously scheduled meetings of the employee
    if organizer_id in emp:
        previous_meetings = emp[organizer_id]
        
# check for clashing previous meetings    
    for meeting in previous_meetings:
        if meeting[0] <= start_time < meeting[1] or meeting[0] < end_time <= meeting[1]:
            return False,1

# schedule the meeting in first vacant room
    for room in rooms:
        if rooms[room] == []:
            rooms[room].append((start_time, end_time))
            emp[organizer_id].append((start_time, end_time))
            return True,0

# if no vacant room, then find the first room with available time slot and schedule the meeting
    for room in rooms:
        meetings = rooms[room]
        flag = 0
        for meeting in meetings:
            if meeting[0] <= start_time < meeting[1] or meeting[0] < end_time <= meeting[1]:
                flag = 1
                break
        if flag == 0:
            rooms[room].append((start_time, end_time))
            emp[organizer_id].append((start_time, end_time))
            return True,0
        
# return false if no meeting room available
    return False,0




### main function to start the meeting scheduler
print("Welcome to Meet Organizer")
M = int(input("Enter the no. of meeting rooms: "))
N = int(input("Enter the number of employees: "))

# dictionaries to store the data of employees and meeting rooms
emp = {}
for i in range(N):
    emp[i] = []
rooms = {}
for i in range(M):
    rooms[i] = []

# loop for calling the functions as per user's choice
while True:
    choice = int(input("\nPress 1 to organize the meeting \nPress 2 to find free time slots \nPress 3 to exit\n"))
    
# to book meeting
    if choice == 1:
        emp_id = int(input("Enter organizer id: "))
        start = int(input("Enter start time: "))
        end = int(input("Enter end time: "))
        x, reason = bookMeeting(emp_id, start, end)
        if x:
            print("Meeting is scheduled successfully!")
        else:
            if reason == 1:
                print("You have other meeting scheduled!")
            else:
                print("No empty meeting room!")
                
# to get the free slots
    elif choice == 2:
        emp_ids = list(map(int, input("Enter list of employees: ").split()))
        start = int(input("Enter start time: "))
        end = int(input("Enter end time: "))
        y = find_free_time_slots(emp_ids, start, end)
        if y == []:
            print("No free time slots found")
        else:
            print("Available free time slots are: ",y)
# exit()            
    else: break
print("Thank you")
