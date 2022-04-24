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

class process:
    def __init__(self, at, bt):
        self.at = int(at)   # arrival time
        self.bt = int(bt)   # burst time
        self.sumofPower = 0 # 소비 전력 합
    def calculate_time(self, time):
        self.tt = time - self.at        # turn-around time
        self.wt = self.tt - self.bt     # waiting time
        self.ntt = self.tt / self.bt    # normalized turn-around time

class processor:
    def __init__(process_input, processor_type="E"):
        self.process = process_input
        self.processor_running = False
        self.type = processor_type
        
        if(self.type == "E"): # E-Core default
            self.processing_per_second = 1      # E Core는 1초에 1의 일을 처리
            self.powerConsuming_per_second = 1  # E Core는 1초에 1의 전력 소비
            self.powerWaiting_per_second = 0.1  # E Core는 1초에 0.1의 대기 전력 소비 (확실치 않음)
        elif(self.type == "P"):  # P-Core Default
            self.processing_per_second = 2      # P Core는 1초에 2의 일을 처리
            self.powerConsuming_per_second = 3  # P Core는 1초에 3의 전력 소비
            self.powerWaiting_per_second = 0.1  # P Core는 1초에 0.1의 대기 전력 소비 (확실치 않음)

    def running_state(process):
        self.processor_running = True                # processor running start
        # ------ running process ------- #
        self.process.bt -= self.processing_per_second       # burst time = processing size
        self.process.bt += self.powerConsuming_per_second   # power consuming
        self.processor_running = False               # processor running finish
        

class FCFS:
    def __init__(self, process_input, processor_input, processor_type):
        self.readyQueue = readyQueue()               # FCFS readyQueue
        self.process = process_input                 # FCFS input process
        self.processor = processor_input             # FCFS input processor
        self.type = processor_type                   # FCFS input processor type

    def ready_state_fcfs(self):
        self.readyQueue_fcfs.enqueue(self.process)  # input된 process를 readyQueue에 삽입
        if(self.processor.processor_running == False): # 작업 중인 process가 없다면
            running_state_fcfs()                     # FCFS running 상태로 돌입

    def running_state_fcfs(self):
        self.ready_process = self.readyQueue.dequeue() # 첫 대기 순번인 process 꺼내기
        while(self.process.bt <= 0):                   # burst time = processing size <= 0 이하가 될 때까지
            self.processor.running_state(self.process) # process running
        terminated_state_fcfs()                        # process finish

    def terminated_state_fcfs(self):
        del self.process
    
    def new_test():
        ysd babo
        
        
