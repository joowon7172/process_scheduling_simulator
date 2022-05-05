import option as op

class HRRN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.CPU = CPU_input
        self.readyQueue = op.HRRN_readyQueue()
        self.time = 0               # 시간 기준 : 0부터 시작

    def running(self):
        count = 0

        while count is not len(self.process):

            # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)):
                if self.process[i].at is not -1 and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].at = -1
                    print("process %d arrive" %(self.process[i].id))

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
                print("process %d finish, total time : %d" %(self.ready_process.id, self.time))

            for ready_p in self.readyQueue.items:          
                if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                    ready_p.wt += 1                             # 도착 시간 wt 증가

        self.terminated_state_hrrn()

    def terminated_state_hrrn(self):
        del self.process