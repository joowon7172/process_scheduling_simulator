# HRRN (High-Response-Ratio-Next)
# Non-preemptive scheduling

class readyQueue:                   # 프로세스들이 기다리는 준비 큐
    def __init__(self):
        self.items = []

    def enqueue(self, items):
        self.items.append(items)    # 프로세스 삽입

    def dequeue(self):
        if not self.isEmpty(): 
            return self.items.pop(0) # 가장 앞에 있는 프로세스 꺼내기

    def isEmpty(self):
        if len(self.items) == 0:
            return True
        else:
            return False

class process:
    def __init__(self, at, bt, num):     # at는 도착 시간, bt는 실행 시간
        self.at = at            # 도착시간(arrive time)   
        self.bt = bt            # 실행시간(burst time)
        self.num = num
        #self.r_ratio = 0
        #self.wt = 0
        #self.tt = 0
        #self.ntt = 0

    def calculate_time(self, time):
        self.tt = time - self.at
        self.wt = self.tt - self.bt
        self.ntt = self.tt / self.bt
    
    def calculate_r_ratio(self):
        self.r_ratio = (self.wt + self.bt) / self.bt    # reponse-ratio 응답률 

    #def input_process(self):
    #    process_list = []
    #    process_list.append(self)

class CPU:
    def __init__(self, process, CPU_type="E"):
        self.process = process
        self.CPU_running = False
        self.type = CPU_type
        self.sumofPower = 0     # 소비 전력 합

        if (self.type == "E"):  # E-Core default
            self.processing_per_second = 1
            self.powerConsuming_per_second = 1
            self.powerWating_per_second = 0.1
        elif (self.type == "P"):    # P-Core 
            self.processing_per_second = 2
            self.powerConsuming_per_second = 3
            self.powerWating_per_second = 0.1 

    def running_state(self, process):
        self.CPU_running = True

        # ------ running process ------
        process.bt -= self.processing_per_second
        self.sumofPower += self.powerConsuming_per_second
        self.CPU_running = False


class HRRN_readyQueue(readyQueue):
    #def __init__(self):
    #    self.items = []

    def HRRN_Priority(self):    # aging 기법 계산을 한 후 응답률이 높은 것부터 작은 순으로 내림차순 정렬
        if self.isEmpty() is not True:
            for i in range (len(self.items) - 2, 0, -1):
                for j in range (0, i+1):
                    if self.items[j].r_ratio < self.items[j+1].r_ratio:
                        self.items[j], self.items[j+1] = self.items[j+1], self.items[j]


class HRRN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.CPU = CPU_input
        self.readyQueue = HRRN_readyQueue()
        self.time = 0               # 시간 기준 : 0부터 시작

    def running_state_hrrn(self):
        count = 0

        while count is not len(self.process):

            # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)):
                if self.process[i].at is not -1 and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].at = -1
                    print("process %d arrive" %(self.process[i].num))

            for p in self.readyQueue.items:
                p.calculate_time(self.time)         # tt, wt, ntt 계산
                p.calculate_r_ratio()               # 응답률(r_ratio) 계산

            self.readyQueue.HRRN_Priority()         # aging 기법에 맞게 우선순위 정렬

            # CPU가 작동중이지 않다면
            if self.CPU.CPU_running is False:
                self.ready_process = self.readyQueue.dequeue()  # 첫 대기 순번인 process 꺼내기
                while(self.ready_process.bt > 0):
                    self.time += 1
                    self.CPU.running_state(self.ready_process)  # process running
                count += 1
                print("process %d finish, total time : %d" %(self.ready_process.num, self.time))

            for ready_p in self.readyQueue.items:          
                if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                    ready_p.wt += 1                             # 도착 시간 wt 증가

        self.terminated_state_hrrn()
    
    def terminated_state_hrrn(self):
        del self.process

if __name__ == "__main__":
    process1 = process(0, 3, 1)
    process2 = process(1, 7, 2)
    process3 = process(3, 2, 3)
    process4 = process(5, 5, 4)
    process5 = process(6, 3, 5)

    process_list = []
    process_list.append(process1)
    process_list.append(process2)
    process_list.append(process3)
    process_list.append(process4)
    process_list.append(process5)
    
    CPU1 = CPU(process_list)
    hrrn_test = HRRN(process_list, CPU1)

    hrrn_test.running_state_hrrn()