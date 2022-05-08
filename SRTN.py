import option as op
import gantt as gt

class SRTN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input # process
        self.readyQueue = op.SRTN_readyQueue() # srtn readyqueue
        self.CPU = CPU_input # processor
        self.type = CPU_input.type # core type
        self.time = 0  # 현재 시간 (lapse)
        self.cnt = 0 # count

        self.gantt = gt.Gantt(len(process_input))  # 간트 차트 클래스 선언
        print("\nTest case started. CPU Type is %s." % self.type)

    def running(self):
        # 모든 프로세스에 대해 수행
        while self.cnt <= len(self.process):
            for i in self.process:  # 프로세스 목록에 있는 프로세스들을 모두 돌아볼때까지
                if i.at == self.time and not i.isUsed:  # 한 프로세스의 AT가 현재 시간과 같고 한 번도 검사받은(= 완료된) 적이 없다면
                    self.readyQueue.enqueue(i)  # 대기 큐에 집어넣음
                    print("process %s has arrived at time %s." % (i.id, self.time))
                    i.isUsed = True
                    self.readyQueue.Priority()  # 대기 큐 한번 정렬.

            self.running_state_srtn()
            
            # 종료 알림
            if self.cnt == len(self.process):
                print("Test case ended.")
                break

    def running_state_srtn(self):
        if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면

            if not self.CPU.CPU_running:  # CPU가 돌아가고 있지 않을 시
                self.readyQueue.Priority()  # 대기 큐 한번 정렬.
                ready_process = self.readyQueue.dequeue()  # 대기 프로세스는 대기 큐에서 dequeue된 프로세스
                self.CPU.CPU_running = True  # 프로세스가 작동 중임을 선언.
                
                print('ready to go %d' % ready_process.id)
                
                start_time = self.time  # 시작 시간 기록.
            
                while ready_process.bt > 0:  # BT가 다 소모되지 않았다면
                    if self.CPU.CPU_running:
                        for j in self.process:  # 한창 돌고 있으면 그 사이 들어올 프로세스 선발
                            if j.at == self.time and not j.isUsed:
                                self.readyQueue.enqueue(j)  # 대기 큐에 집어넣음
                                print("process %s has arrived at time %s." % (j.id, self.time))
                                j.isUsed = True  # 뽑았으니까 일단 플래그 세우기
                                self.readyQueue.Priority()  # 대기 큐 한번 정렬.

                                preemption_time = self.time  # 선점당한 시간 기록

                                if j.bt < ready_process.bt:  # 새로 도착한 프로세스가 돌아가고 있는 프로세스보다 bt가 작다면 선점.
                                    ready_process = self.preemption(ready_process, start_time)
                                    ready_process.isUsed = True
                                    start_time = preemption_time

                                elif j.bt == ready_process.bt:  # bt가 같은 경우 at가 먼저인 걸 (먼저 도착한걸) 우선하여 작업.
                                    if j.at <= ready_process.at:
                                        ready_process = self.preemption(ready_process, start_time)
                                        ready_process.isUsed = True
                                        start_time = preemption_time

                        ready_process.bt -= self.CPU.processing_per_second  # CPU의 작업능률만큼 bt 소모
                        print("Running %s... BT remains %s. Time is %s." % (ready_process.id, str(ready_process.bt), self.time))
                        self.CPU.sumofPower += self.CPU.powerConsuming_per_second  # 소모전력 (어디다 쓰는지 모름)

                    else:
                        self.CPU.sumofPower += self.CPU.powerWaiting_per_second  # 대기전력 (작업을 안 할 동안 소모되는 전력?)

                    self.time += 1  # 한 작업 완수 시마다 시간 초 증가.

                    # GUI 용 WT 계산
                    for ready_p in self.readyQueue.items:          
                        if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                            ready_p.wt += 1                             # 대기 시간 wt 증가
                
                # GUI 용 TT, NTT 계산
                ready_process.tt = ready_process.wt + ready_process.tmp_bt
                ready_process.ntt = round(ready_process.tt / ready_process.tmp_bt, 3)

                self.CPU.CPU_running = False  # 작업 종료 시 CPU 플래그 끄기

                if ready_process.bt <= 0:  # 작업이 끝난 프로세스의 BT가 0이고 대기 큐에서 완전히 지워졌다면 종료 메시지
                    self.termination_state_srtn(ready_process, start_time)

        else:  # 작업 중 대기 큐에 아직 도착한 프로세스가 없거나 할 때
            self.time += 1  # 시간만 +1 해줌.
            self.CPU.sumofPower += self.CPU.powerWaiting_per_second  # 대기전력 (작업을 안 할 동안 소모되는 전력?)
            print("No process in ready queue. Time is %s." % self.time)

    def termination_state_srtn(self, ready_process, start_time):  # 작업이 끝난 프로세스 termination.
        print("Process %s ended at time %s." % (ready_process.id, self.time))
        self.gantt.store(start_time, self.time, ready_process.id)  # 간트 차트에 표시할 정보 저장.
        del ready_process
        self.cnt += 1

    def preemption(self, ready_process, start_time):  # 선점 함수
        self.gantt.store(start_time, self.time, ready_process.id)  # 간트 차트에 표시할 정보 저장.
        ready_process.isUsed = False  # 다시 뽑혀야 되므로 검진 플래그 끄기
        self.readyQueue.enqueue(ready_process)  # 다시 큐로 들여보냄.
        new = self.readyQueue.dequeue()
        print("process %s was preempted by process %s, which has entered instead." % (ready_process.id, new.id))
        return new  # 새로 도착한 프로세스를 준비시킴.