# FCFS (First-Come-First-Service)
# Non-preemptive
# ready queue criteria
class readyQueue:
    def __init__(self):
        self.items = []
    
    def enqueue(self, items):
        self.items.append(items)    # 삽입

    def dequeue(self):
        if not self.isEmpty(): return self.items.pop(0) # 꺼내기
    
    def isEmpty(self):
        if len(self.items) == 0:
            return True
        else: return False

class process:
    def __init__(self, at, bt):
        self.at = at   # arrival time
        self.bt = bt   # burst time
        self.sumofPower = 0 # 소비 전력 합
    def calculate_time(self, time):
        self.tt = time - self.at        # turn-around time
        self.wt = self.tt - self.bt     # waiting time
        self.ntt = self.tt / self.bt    # normalized turn-around time

class SPN_readyQueue(readyQueue):
    def __init__(self):
        self.items = []

    def SPN_Priority(self): # 버블 정렬을 이용해 bt가 작은 순으로 오름차순 정렬
        for j in range (len(self.items), 1, -1):
            for i in range (0, j-1):
                if self.items[i].bt > self.items[i+1].bt:
                    self.items[i], self.items[i+1] = self.items[i+1], self.items[i]

class CPU:
    def __init__(self, process, CPU_type="E"):
        self.process = process
        self.CPU_running = False
        self.type = CPU_type
        
        if(self.type == "E"): # E-Core default
            self.processing_per_second = 1      # E Core는 1초에 1의 일을 처리
            self.powerConsuming_per_second = 1  # E Core는 1초에 1의 전력 소비
            self.powerWaiting_per_second = 0.1  # E Core는 1초에 0.1의 대기 전력 소비 (확실치 않음)
        elif(self.type == "P"):  # P-Core Default
            self.processing_per_second = 2      # P Core는 1초에 2의 일을 처리
            self.powerConsuming_per_second = 3  # P Core는 1초에 3의 전력 소비
            self.powerWaiting_per_second = 0.1  # P Core는 1초에 0.1의 대기 전력 소비 (확실치 않음)

    def running_state(self, process):
        self.CPU_running = True                # CPU running start
        # ------ running process ------- #
        process.bt -= self.processing_per_second       # burst time = processing size
        print("running 수행중", process)
        self.CPU_running = False               # CPU running finish
        

class FCFS:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.readyQueue = readyQueue()               # FCFS readyQueue
        self.CPU = CPU_input             # FCFS input CPU
        self.type = CPU_input.type                # FCFS input CPU type

    def ready_state_fcfs(self):
        self.readyQueue.enqueue(self.process)  # input된 process를 readyQueue에 삽입
        if(self.CPU.CPU_running == False): # 작업 중인 process가 없다면
            print("통과했니??dd")
            self.running_state_fcfs()                     # FCFS running 상태로 돌입

    def running_state_fcfs(self):
        self.ready_process = self.readyQueue.dequeue() # 첫 대기 순번인 process 꺼내기
        while(self.ready_process.bt > 0):
            print("ddd")                   # burst time = processing size <= 0 이하가 될 때까지
            self.CPU.running_state(self.ready_process) # process running
        print("burst time end!!?!??!")
        self.terminated_state_fcfs()                        # process finish

    def terminated_state_fcfs(self):
        del self.process

class SPN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.CPU = CPU_input             # FCFS input CPU
        self.readyQueue = SPN_readyQueue()

    def ready_state_spn(self):
        for i in range(0, len(self.process)):
            self.readyQueue.enqueue(self.process[i])
            print(self.readyQueue.items)
        if(len(self.readyQueue.items) > 1): # readyQueue에 Process가 2개 이상 있을 경우
            self.readyQueue.SPN_Priority() # Priority에 맞게 정렬
            print(self.readyQueue.items)
        if self.CPU.CPU_running is False:
            self.running_state_spn()

    def running_state_spn(self):
        # print("test")
        # print(self.readyQueue.items)
        while self.readyQueue.isEmpty() is not True:
            self.ready_process = self.readyQueue.dequeue() # 첫 대기 순번인 process 꺼내기
            # print(self.readyQueue.items)
            # print(self.ready_process)
            while(self.ready_process.bt > 0):
                self.CPU.running_state(self.ready_process) # process running
            print("process finish")
        self.terminated_state_spn()                        # process finish
        # print("If escape the loop")
    def terminated_state_spn(self):
        del self.process

  
        
if __name__ == "__main__":
    process1 = process(0, 3)
    CPU1 = CPU(process1, "E")
    fcfs1 = FCFS(process1, CPU1)
    #fcfs1.ready_state_fcfs()
    process2 = process(1, 6)
    process3 = process(2, 4)
    process4 = process(3, 1)
    process5 = process(6, 2)
    process6 = process(2, 5)

    process_list = []
    process_list.append(process1)
    process_list.append(process2)
    process_list.append(process3)
    process_list.append(process4)
    process_list.append(process5)
    process_list.append(process6)
    
    spn_test = SPN(process_list, CPU1)

    spn_test.ready_state_spn()
