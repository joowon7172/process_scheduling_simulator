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
                    print("process %d arrive. Time is %d." %(self.process[i].id, self.time))

            self.readyQueue.Priority() # Priority에 맞게 정렬

            # CPU가 작동중이지 않다면
            if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면     
                if self.CPU.CPU_running is False:
                    self.ready_process = self.readyQueue.dequeue() # 첫 대기 순번인 process 꺼내기
                    while self.ready_process.bt > 0:
                        if self.ready_process.bt == 0:  # 해당 프로세스의 BT가 다 소모되면 반복 탈출.
                            break
                        else:
                            self.time += 1
                            self.CPU.running_state(self.ready_process) # process running
                            for i in range(0, len(self.process)): 
                                if self.process[i].at is not -1 and self.process[i].at == self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].at = -1 # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive. Time is %d." %(self.process[i].id, self.time))
                            self.readyQueue.Priority() # Priority에 맞게 정렬
                    count += 1
                    if self.ready_process.bt == 0 and self.ready_process not in self.readyQueue.items:
                        self.terminated_state_spn(self.ready_process)                        # process finish
            else:  # 작업 중 대기 큐에 아직 도착한 프로세스가 없거나 할 때
                self.time += 1  # 시간만 +1 해줌.
                self.CPU.sumofPower += self.CPU.powerWaiting_per_second  # 대기전력 (작업을 안 할 동안 소모되는 전력?)
                print("No process in ready queue. Time is %s." % self.time)

        print(self.CPU.sumofPower)
    
    def terminated_state_spn(self, ready_process):
        print("process %d finish, total time : %d" %(ready_process.id, self.time))
        del self.ready_process