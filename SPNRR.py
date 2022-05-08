# SPN과 RR의 합성
# 버스트타임(bt)를 고려한 다음 타임퀀텀(tq)을 설정해서 무한 대기 현상 최소화
# 평균대기시간 최소화
# 타임퀀텀이 클수록 SPN이 된다.
# 많은 프로세스들에게 빠른 응답시간 제공
# 타임퀀텀이 작을수록 오버헤드가 큼

# SPNRR
# Half Preemptive scheduling (반선점 방식)
# 자원 사용시간 제한 (time quantum) 있음
# 프로세스가 종료되면 SPN 우선순위 정렬
import option as op
import gantt as gt

# 정해진 타임퀀텀만큼 CPU를 할당하고 작업을 완료하지 못하면 ready queue의 맨 뒤에 삽입되어 자기차례를 기다림
class SPNRR:
    
    def __init__(self, process_input, CPU_input, tq):
        self.process = process_input    # process_input 값을 SPNRR클래스의 process로 설정
        self.CPU = CPU_input            # CPU_input 값을 SPNRR클래스의 CPU로 설정
        self.readyQueue = op.SPNRR_readyQueue()   # SPNRR_readyQueue() 함수를 SPNRR클래스의 readyQueue 변수로 설정
        self.tq = tq                # time quantum
        self.time = 0               # 시간 기준 : 0부터 시작
        self.gantt = gt.Gantt(len(process_input))

    # 스케쥴링 기준이 먼저 도착한 순서임
    def running(self): 
        count = 0

        while count is not len(self.process):
            
           # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)): 
                if self.process[i].isUsed is False and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].isUsed = True # 이미 추가된 프로세스 예외처리
                    print("process %d arrive" %(self.process[i].id))
            
            if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면
                if self.CPU.CPU_running is False: # CPU가 작동중이지 않다면
                    self.ready_process = self.readyQueue.dequeue() # 대기큐 맨 앞의 process 꺼내기
                    
                    start_time = self.time # 간트 시간 저장
                    
                    #bt가 tq보다 커서 해당 프로세스의 일이 끝나지 않았으면
                    if(self.ready_process.bt - self.tq > 0): 
                        cnt = 0 # time quantum 크기만큼 돌리기위해 세는 cnt변수
                        
                        # tq만큼만 프로세스가 처리
                        while(self.tq != cnt):
                            self.time += 1
                            self.CPU.running_state(self.ready_process) # process running
                            cnt += 1
                            
                            # 현재시간과 도착시간을 비교하여 삽입
                            for i in range(0, len(self.process)): 
                                if self.process[i].isUsed is False and self.process[i].at <= self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].isUsed = True # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive" %(self.process[i].id))
                            
                            # GUI 용 WT 계산
                            for ready_p in self.readyQueue.items:          
                                if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                                    ready_p.wt += 1                             # 대기 시간 wt 증가 
                        
                        self.gantt.store(start_time, self.time, self.ready_process.id) # 간트 정보 저장

                        self.readyQueue.enqueue(self.ready_process) # 대기큐 맨뒤에 넣기

                    #bt가 tq보다 같거나 작아서 tq크기 안에서 프로세스 일이 끝났을때
                    elif(self.ready_process.bt - self.tq <= 0):
                        
                        # bt가 tq보다 작아서 한번에 실행될 때
                        while(self.ready_process.bt > 0):
                            self.time += 1
                            self.CPU.running_state(self.ready_process) # process running
                            
                            # 현재시간과 도착시간을 비교하여 삽입
                            for i in range(0, len(self.process)): 
                                if self.process[i].isUsed is False and self.process[i].at <= self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].isUsed = True # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive" %(self.process[i].id))
                            
                            # GUI 용 WT 계산
                            for ready_p in self.readyQueue.items:          
                                if ready_p.at < self.time and ready_p.bt != 0:  # 레디 큐에 도착은 했지만 프로세서에 들어가지 못하고 대기중인 프로세스에 대해
                                    ready_p.wt += 1                             # 대기 시간 wt 증가
                                
                        # GUI 용 TT, NTT 계산
                        self.ready_process.tt = self.ready_process.wt + self.ready_process.tmp_bt
                        self.ready_process.ntt = round(self.ready_process.tt / self.ready_process.tmp_bt, 3)
                        
                        self.readyQueue.Priority() # priority 호출
                        
                        print("process %d finish, total time : %d" %(self.ready_process.id, self.time))
                        
                        # 간트 예외처리
                        if self.time - start_time != 0:
                            self.gantt.store(start_time, self.time, self.ready_process.id)

                        count += 1

            # 작업이 끝난 프로세스의 BT가 0이고 대기 큐에서 완전히 지워졌다면 종료 메시지            
            if self.ready_process.bt == 0 and self.ready_process not in self.readyQueue.items:  
                self.terminated_state_SPNRR(self.ready_process, start_time)        


    def terminated_state_SPNRR(self, ready_process, start_time): # 종료
        self.gantt.store(start_time, self.time, ready_process.id) # 간트 정보 저장
        print("Process %s ended at time %s." % (ready_process.id, self.time) )
        del self.ready_process