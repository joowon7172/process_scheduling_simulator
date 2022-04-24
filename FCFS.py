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

class process:
    def __init__(self, at, bt):
        self.at = at   # arrival time
        self.bt = bt   # burst time
        self.sumofPower = 0 # 소비 전력 합
    def calculate_time(self, time):
        self.tt = time - self.at        # turn-around time
        self.wt = self.tt - self.bt     # waiting time
        self.ntt = self.tt / self.bt    # normalized turn-around time

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
        CPU.CPU_running = True                # CPU running start
        # ------ running process ------- #
        process.bt -= self.processing_per_second       # burst time = processing size
        print("running 수행중")
        CPU.CPU_running = False               # CPU running finish
        

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
        print("burst time end")
        self.terminated_state_fcfs()                        # process finish

    def terminated_state_fcfs(self):
        del self.process

if __name__ == "__main__":
    process1 = process(0, 10)
    CPU1 = CPU(process1, "E")
    fcfs1 = FCFS(process1, CPU1)
    fcfs1.ready_state_fcfs()


