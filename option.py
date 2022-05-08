class readyQueue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, items):
        self.items.append(items)    # 삽입

    def dequeue(self):
        if not self.isEmpty(): return self.items.pop(0) # 꺼내기
    
    def isEmpty(self): # 비었는가?
        if len(self.items) == 0:
            return True
        else: return False

    def peek(self):  # 다음 프로세스 미리보기
        if not self.isEmpty():
            return self.items[0]
        else:
            return False


class process: # 프로세스
    def __init__(self, at, bt, id):
        self.at = at   # arrival time
        self.bt = bt   # burst time
        self.id = id   # id
        self.wt = 0    # waiting time
        self.tt = 0    # turn around time
        self.ntt = 0   # normalized turn around time
        self.isUsed = False # 예외처리
        self.tmp_at = at    # gui용 at
        self.tmp_bt = bt    # gui용 bt
    # def calculate_time(self, time):
    #     self.tt = time - self.tmp_at        # turn-around time
    #     self.wt = self.tt - self.tmp_bt     # waiting time
    #     self.ntt = round(self.tt / self.tmp_bt, 3)    # normalized turn-around time
    def calculate_r_ratio(self):
        self.r_ratio = (self.wt + self.tmp_bt) / self.tmp_bt # reponse-ratio 응답률

class SPN_readyQueue(readyQueue): # spn readyqueue
    def __init__(self):
        self.items = []

    def Priority(self): # 버블 정렬을 이용해 bt가 작은 순으로 오름차순 정렬
        if self.isEmpty() is not True:
            for j in range (len(self.items), 0, -1):
                for i in range (0, j-1):
                    if self.items[i].bt > self.items[i+1].bt:
                        self.items[i], self.items[i+1] = self.items[i+1], self.items[i]

class SRTN_readyQueue(SPN_readyQueue): # srtn readyqueue
    pass

class HRRN_readyQueue(readyQueue): # hrrn readyqueue
    def HRRN_Priority(self):    # aging 기법 계산을 한 후 응답률이 높은 것부터 작은 순으로 내림차순 정렬
        if self.isEmpty() is not True:
            for i in range (len(self.items) - 2, 0, -1):
                for j in range (0, i+1):
                    if self.items[j].r_ratio < self.items[j+1].r_ratio:
                        self.items[j], self.items[j+1] = self.items[j+1], self.items[j]

class RR_readyQueue(readyQueue): # rr readyqueue
    def RR_Priority(self): ## rr priority
        pass

class SPNRR_readyQueue(readyQueue): # spn rr readyqueue
    def Priority(self): # 버블 정렬을 이용해 bt가 작은 순으로 오름차순 정렬
        if self.isEmpty() is not True:
            for j in range (len(self.items), 0, -1):
                for i in range (0, j-1):
                    if self.items[i].bt > self.items[i+1].bt:
                        self.items[i], self.items[i+1] = self.items[i+1], self.items[i]
                        
class CPU: # processor
    def __init__(self, process, CPU_type="E"):
        self.process = process # process
        self.CPU_running = False # cpu running check
        self.type = CPU_type # cpu core type
        self.sumofPower = 0 # 소비 전력 합

        
        if(self.type == "E"): # E-Core default
            self.processing_per_second = 1      # E Core는 1초에 1의 일을 처리
            self.powerConsuming_per_second = 1  # E Core는 1초에 1의 전력 소비
            self.powerWaiting_per_second = 0.1  # E Core는 1초에 0.1의 대기 전력 소비 (확실치 않음)
        elif(self.type == "P"):  # P-Core Default
            self.processing_per_second = 2      # P Core는 1초에 2의 일을 처리
            self.powerConsuming_per_second = 3  # P Core는 1초에 3의 전력 소비
            self.powerWaiting_per_second = 0.1  # P Core는 1초에 0.1의 대기 전력 소비 (확실치 않음)

    def running_state(self, process): # cpu running
        self.CPU_running = True                # CPU running start
        # ------ running process ------- #
        process.bt -= self.processing_per_second       # burst time = processing size
        self.sumofPower += self.powerConsuming_per_second # 소비 전력 계산
        self.CPU_running = False               # CPU running finish
    
