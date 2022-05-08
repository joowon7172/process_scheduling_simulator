import option as op
import gantt as gt


class FCFS:
    def __init__(self, process_input, CPU_input):
        self.process = process_input # process
        self.readyQueue = op.readyQueue()  # FCFS readyQueue
        self.CPU = CPU_input  # FCFS input CPU
        self.time = 0  # 시간 기준을 잡기 위함
        self.gantt = gt.Gantt(len(process_input))

    def running(self):
        count = 0

        # 모든 프로세스에 대해 수행
        while count != len(self.process):
            # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)):
                if self.process[i].isUsed is False and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].isUsed = True  # 이미 추가된 프로세스 예외처리
                    print("process %d arrive. Time is %d." % (self.process[i].id, self.time))

            # CPU가 작동중이지 않다면
            if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면     
                if self.CPU.CPU_running is False:
                    self.ready_process = self.readyQueue.dequeue()  # 첫 대기 순번인 process 꺼내기
                    start_time = self.time
                    while self.ready_process.bt > 0:
                        if self.ready_process.bt == 0:  # 해당 프로세스의 BT가 다 소모되면 반복 탈출.
                            break
                        else:
                            self.time += 1
                            self.CPU.running_state(self.ready_process)  # process running
                            # 현재시간과 도착시간을 비교하여 삽입
                            for i in range(0, len(self.process)):
                                if self.process[i].isUsed is False and self.process[i].at == self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].isUsed = True  # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive. Time is %d." % (self.process[i].id, self.time))
                            
                            # GUI 용 WT 계산
                            for ready_p in self.readyQueue.items:          
                                if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                                    ready_p.wt += 1                             # 대기 시간 wt 증가
                                   
                    # GUI 용 TT, NTT 계산
                    self.ready_process.tt = self.ready_process.wt + self.ready_process.tmp_bt
                    self.ready_process.ntt = round(self.ready_process.tt / self.ready_process.tmp_bt, 3)

                    count += 1
                    if self.ready_process.bt <= 0 and self.ready_process not in self.readyQueue.items:
                        self.terminated_state_fcfs(self.ready_process, start_time)  # process finish

            else:  # 작업 중 대기 큐에 아직 도착한 프로세스가 없거나 할 때
                self.time += 1  # 시간만 +1 해줌.
                self.CPU.sumofPower += self.CPU.powerWaiting_per_second  # 대기전력 (작업을 안 할 동안 소모되는 전력?)
                print("No process in ready queue. Time is %s." % self.time)

        print("Sum of Power Consuming :", self.CPU.sumofPower)

    def terminated_state_fcfs(self, ready_process, start_time): # 종료
        self.gantt.store(start_time, self.time, ready_process.id) # 간트 정보 저장
        print("process %d finish, total time : %d" % (ready_process.id, self.time))
        del self.ready_process