import option as op

class SPN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.CPU = CPU_input             # FCFS input CPU
        self.readyQueue = op.SPN_readyQueue()
        self.time = 0 # 시간 기준을 잡기 위함

    def running(self):
        count = 0

        while count is not len(self.process):
            
            # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)): 
                if self.process[i].at is not -1 and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].at = -1 # 이미 추가된 프로세스 예외처리
                    print("process %d arrive" %(self.process[i].id))
            
            self.readyQueue.Priority() # Priority에 맞게 정렬

            # CPU가 작동중이지 않다면
            if self.CPU.CPU_running is False:
                self.ready_process = self.readyQueue.dequeue() # 첫 대기 순번인 process 꺼내기
                while(self.ready_process.bt > 0):
                    self.time += 1
                    self.CPU.running_state(self.ready_process) # process running
                count += 1
                print("process %d finish, total time : %d" %(self.ready_process.id, self.time))
        
        self.terminated_state_spn()                        # process finish
    
    def terminated_state_spn(self):
        del self.process