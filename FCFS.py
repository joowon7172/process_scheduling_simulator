import option as op

class FCFS:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.readyQueue = op.readyQueue()               # FCFS readyQueue
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