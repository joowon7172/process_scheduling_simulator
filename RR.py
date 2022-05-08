# RR(Round Robin)
# Preemptive scheduling (선점 방식)
# 자원 사용시간 제한 (time quantum) 있음
# 도착시간 순으로

import option as op
import gantt as gt

# 정해진 타임퀀텀만큼 CPU를 할당하고 작업을 완료하지 못하면 ready queue의 맨 뒤에 삽입되어 자기차례를 기다림
class RR:

    def __init__(self, process_input, CPU_input, tq):
        self.process = process_input  # process_input 값을 RR클래스의 process로 설정
        self.CPU = CPU_input  # CPU_input 값을 RR클래스의 CPU로 설정
        self.readyQueue = op.RR_readyQueue()  # RR_readyQueue() 함수를 RR클래스의 readyQueue 변수로 설정
        self.tq = tq # time quantum
        self.time = 0  # 시간 기준 : 0부터 시작

        self.gantt = gt.Gantt(len(process_input))

    def running(self):
        if not self.CPU.CPU_running:  # 작업 중인 process가 없다면            
            self.running_state_RR()  # RR running 상태로 돌입

    # 스케쥴링 기준이 먼저 도착한 순서임
    def running_state_RR(self):
        count = 0
        # 모든 프로세스에 대해 수행
        while count is not len(self.process):
            # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)):
                if self.process[i].isUsed is False and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].isUsed = True  # 이미 추가된 프로세스 예외처리
                    print("process %d arrive" % self.process[i].id)
            start_time = self.time
            # CPU가 작동중이지 않다면
            if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면
                if self.CPU.CPU_running is False:
                    self.ready_process = self.readyQueue.dequeue()  # 대기큐 맨 앞의 process 꺼내기
                    if self.ready_process.bt - self.tq > 0:  # bt가 tq보다 커서 해당 프로세스의 일이 끝나지 않았으면       
                        cnt = 0  # time quantum 크기만큼 돌리기위해 세는 cnt변수
                        
                        # tq만큼만 프로세스가 처리
                        while self.tq != cnt:
                            self.time += 1
                            self.CPU.running_state(self.ready_process)  # process running
                            cnt += 1
                            
                            # 현재시간과 도착시간을 비교하여 삽입
                            for i in range(0, len(self.process)):
                                if self.process[i].isUsed is False and self.process[i].at <= self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].isUsed = True  # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive" % self.process[i].id)
                            
                            # GUI 용 WT 계산
                            for ready_p in self.readyQueue.items: 
                                if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                                    ready_p.wt += 1                             # 대기 시간 wt 증가
                        
                        print("%d returned to the queue at time %d" % (self.ready_process.id, self.time))
                        self.gantt.store(start_time, self.time, self.ready_process.id) # 간트 정보 저장

                        self.readyQueue.enqueue(self.ready_process)  # 대기큐 맨뒤에 넣기

                    # bt가 tq보다 같거나 작아서 tq크기 안에서 프로세스 일이 끝났을때
                    elif self.ready_process.bt - self.tq <= 0:
                        
                        # bt가 tq보다 작아서 한번에 실행될 때
                        while self.ready_process.bt > 0:
                            self.time += 1
                            self.CPU.running_state(self.ready_process)  # process running
                            
                            # 현재시간과 도착시간을 비교하여 삽입
                            for i in range(0, len(self.process)):
                                if self.process[i].isUsed is False and self.process[i].at <= self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].isUsed = True  # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive" % self.process[i].id)
                            
                            # GUI 용 WT 계산
                            for ready_p in self.readyQueue.items:          
                                if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                                    ready_p.wt += 1                             # 대기 시간 wt 증가
                        
                        # GUI 용 TT, NTT 계산
                        self.ready_process.tt = self.ready_process.wt + self.ready_process.tmp_bt
                        self.ready_process.ntt = round(self.ready_process.tt / self.ready_process.tmp_bt, 3)
                        
                        print("process %d finish, total time : %d" % (self.ready_process.id, self.time))
                        
                        # 간트 예외처리
                        if self.time - start_time != 0:
                            self.gantt.store(start_time, self.time, self.ready_process.id)
                        count += 1

                # 작업이 끝난 프로세스의 BT가 0이고 대기 큐에서 완전히 지워졌다면 종료 메시지
                if self.ready_process.bt == 0 and self.ready_process not in self.readyQueue.items:
                    self.terminated_state_RR(self.ready_process, start_time)

    def terminated_state_RR(self, ready_process, start_time): # 종료
        self.gantt.store(start_time, self.time, ready_process.id) # 간트 정보 저장
        print("Process %s ended at time %s." % (ready_process.id, self.time))
        del self.ready_process