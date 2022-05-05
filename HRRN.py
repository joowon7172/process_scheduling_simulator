import option as op

class HRRN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.CPU = CPU_input
        self.type = CPU_input.type
        self.readyQueue = op.HRRN_readyQueue()
        self.time = 0               # 시간 기준 : 0부터 시작
        self.cnt = 0

        print("\nTest case started. CPU Type is %s." % self.type)

    def running(self):
        while self.cnt <= len(self.process):
            # 현재시간과 도착시간을 비교하여 삽입
            for i in self.process:
                if i.at is not -1 and i.at <= self.time:
                    self.readyQueue.enqueue(i)
                    print("process %d arrive at time %s" % (i.id, self.time))
                    i.at = -1

            if self.cnt == len(self.process):
                    print("Test case ended.")
                    break

            if self.readyQueue.peek():
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
                        
                        for i in self.process:
                            if i.at is not -1 and i.at <= self.time:
                                self.readyQueue.enqueue(i)
                                print("process %d arrive at time %s" % (i.id, self.time))
                                i.at = -1

                        for ready_p in self.readyQueue.items:          
                            if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                                ready_p.wt += 1                             # 도착 시간 wt 증가

                    self.cnt += 1
                    print("process %d finish, total time : %d" %(self.ready_process.id, self.time))
                    
                    if self.ready_process.bt == 0 and self.ready_process not in self.readyQueue.items:  # 작업이 끝난 프로세스의 BT가 0이고 대기 큐에서 완전히 지워졌다면 종료 메시지
                        self.terminated_state_hrrn(self.ready_process)
            
            else:
                self.time += 1                                      # 시간 +1
                self.CPU.sumofPower += self.CPU.powerWaiting_per_second      # 대기전력 (작업을 안 할 동안 소비되는 전력)    

    def terminated_state_hrrn(self, ready_process):
        print("Process %s ended at time %s." % (ready_process.id, self.time) )
        del self.ready_process

