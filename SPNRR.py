# SPN과 RR의 합성
# 버스트타임(bt)를 고려한 다음 타임퀀텀(tq)을 설정해서 무한 대기 현상 최소화
# 평균대기시간 최소화
# 타임퀀텀이 클수록 SPN이 된다.
# 많은 프로세스들에게 빠른 응답시간 제공
# 타임퀀텀이 작을수록 오버헤드가 큼

# SPNRR
# Half Preemptive scheduling (반선점 방식)
# 자원 사용시간 제한 (time quantum) 있음
# 프로세스가 종료되면 SRN 우선순위 정렬
import option as op

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
        else: return False

    def peek(self):  # 다음 프로세스 미리보기
        if not self.isEmpty():
            return self.items[0]
        else:
            return False


class process:
    def __init__(self, at, bt, id, tq):
        self.at = at   # arrival time
        self.bt = bt   # burst time
        self.id = id
        self.tq = tq

    def calculate_time(self, time):
        self.tt = time - self.at        # turn-around time
        self.wt = self.tt - self.bt     # waiting time
        self.ntt = self.tt / self.bt    # normalized turn-around time
       
    
    
class CPU:
    def __init__(self, process, CPU_type="P"):
        self.process = process
        self.CPU_running = False
        self.type = CPU_type
        self.sumofPower = 0     # 소비 전력 합

        if (self.type == "E"):  # E-Core default
            self.processing_per_second = 1      # 1초에 1의 일을 처리
            self.powerConsuming_per_second = 1  # 1초당 전력 1 소비
            self.powerWating_per_second = 0.1   # 초당 0.1 대기전력
        elif (self.type == "P"):    # P-Core 
            self.processing_per_second = 2  # 1초에 2의 일을 처리
            self.powerConsuming_per_second = 3  # 1초당 전력 3 소비
            self.powerWating_per_second = 0.1 # 초당 0.1 대기전력

    # 실행 상태
    def running_state(self, process):
        self.CPU_running = True

        # ------ running process ------
        # 여기서 프로세싱 작업 하면서 bt가 점점 깎여나감
        process.bt -= self.processing_per_second    # 실행시간 = 실행시간 - 1초에 처리하는 일                                                    
                                                    # burst time = processing size
        self.sumofPower += self.powerConsuming_per_second   #전력소비 합
        self.CPU_running = False


class SPNRR_readyQueue(readyQueue):
    
    # def __init__(self):
    #     self.items = []

    def Priority(self): # 버블 정렬을 이용해 bt가 작은 순으로 오름차순 정렬
        if self.isEmpty() is not True:
            for j in range (len(self.items), 0, -1):
                for i in range (0, j-1):
                    if self.items[i].bt > self.items[i+1].bt:
                        #if (self.items[i].bt < self.items[i].tq):
                        #     return
                        # else:
                        self.items[i], self.items[i+1] = self.items[i+1], self.items[i]


# 정해진 타임퀀텀만큼 CPU를 할당하고 작업을 완료하지 못하면 ready queue의 맨 뒤에 삽입되어 자기차례를 기다림
class SPNRR:
    
    def __init__(self, process_input, CPU_input):
        self.process = process_input    # process_input 값을 SPNRR클래스의 process로 설정
        self.CPU = CPU_input            # CPU_input 값을 SPNRR클래스의 CPU로 설정
        self.readyQueue = SPNRR_readyQueue()   # SPNRR_readyQueue() 함수를 SPNRR클래스의 readyQueue 변수로 설정

        self.time = 0               # 시간 기준 : 0부터 시작

    def ready_state_SPNRR(self):
        self.readyQueue.enqueue(self.process)  # input된 process를 readyQueue에 삽입

        if(self.CPU.CPU_running == False): # 작업 중인 process가 없다면
            #print("통과했니??dd")
            self.running_state_SPNRR()        # SPNRR running 상태로 돌입


    

    # 스케쥴링 기준이 먼저 도착한 순서임
    def running_state_SPNRR(self): 
        count = 0
        p_cnt = 0
        while count is not len(self.process):
            
           # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)): 
                if self.process[i].at != -1 and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].at = -1 # 이미 추가된 프로세스 예외처리
                    print("process %d arrive" %(self.process[i].id))

            # 처음 한번만 정렬
            #if p_cnt == 0:
                #self.readyQueue.Priority()
            #p_cnt = 1

            # CPU가 작동중이지 않다면
            if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면
                if self.CPU.CPU_running is False:
                    self.ready_process = self.readyQueue.dequeue() # 대기큐 맨 앞의 process 꺼내기

                    #bt가 tq보다 커서 해당 프로세스의 일이 끝나지 않았으면
                    if(self.ready_process.bt - self.ready_process.tq > 0): 
                        #print("process start")
                        cnt = 0 # time quantum 크기만큼 돌리기위해 세는 cnt변수
                        while(self.ready_process.tq != cnt):
                            self.time += 1
                            self.CPU.running_state(self.ready_process) # process running
                            cnt += 1
                            for i in range(0, len(self.process)): 
                                if self.process[i].at != -1 and self.process[i].at <= self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].at = -1 # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive" %(self.process[i].id))
                         
                        #self.readyQueue.Priority()
                        print("일이 덜 끝났으므로 다시 대기큐에 들어가")
                        #print("process %d go inside readyqueue" %(self.process[i].id))
                        self.readyQueue.enqueue(self.ready_process) # 대기큐 맨뒤에 넣기

                    #bt가 tq보다 같거나 작아서 tq크기 안에서 프로세스 일이 끝났을때
                    elif(self.ready_process.bt - self.ready_process.tq <= 0):
                        #print("process start")
                        while(self.ready_process.bt > 0):
                            self.time += 1
                            self.CPU.running_state(self.ready_process) # process running
                            #self.readyQueue.enqueue(self.ready_process) # 대기큐 맨뒤에 넣기
                            for i in range(0, len(self.process)): 
                                if self.process[i].at != -1 and self.process[i].at <= self.time:
                                    self.readyQueue.enqueue(self.process[i])
                                    self.process[i].at = -1 # 이미 추가된 프로세스 예외처리
                                    print("process %d arrive" %(self.process[i].id))
                        self.readyQueue.Priority()
                        print("process %d finish, total time : %d" %(self.ready_process.id, self.time))
                        count += 1

            # 작업이 끝난 프로세스의 BT가 0이고 대기 큐에서 완전히 지워졌다면 종료 메시지            
            if self.ready_process.bt == 0 and self.ready_process not in self.readyQueue.items:  
                self.terminated_state_SPNRR(self.ready_process)        


    def terminated_state_SPNRR(self, ready_process):
        print("Process %s ended at time %s." % (ready_process.id, self.time) )
        del self.ready_process


if __name__ == "__main__":
    
    process1 = process(0, 3, 1, 3)
    process2 = process(1, 7, 2, 3)
    process3 = process(3, 2, 3, 3)
    process4 = process(5, 5, 4, 3)
    process5 = process(6, 3, 5, 3)

    process_list = []
    process_list.append(process1)
    process_list.append(process2)
    process_list.append(process3)
    process_list.append(process4)
    process_list.append(process5)
    
    CPU1 = CPU(process_list)
    SPNRR_test = SPNRR(process_list, CPU1)

    SPNRR_test.running_state_SPNRR()