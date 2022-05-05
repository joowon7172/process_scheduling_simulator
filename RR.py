# RR(Round Robin)
# Preemptive scheduling (선점 방식)
# 자원 사용시간 제한 (time quantum) 있음
# 도착시간 순으로
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
    def __init__(self, at, bt, tq):     # at는 도착 시간, bt는 실행 시간, tq는 CPU 할당 시간
        self.at = at            # 도착시간(arrive time)   
        self.bt = bt            # 실행시간(burst time)
        self.tq = tq            # CPU 할당 시간(time quantum)
        

    def calculate_time(self, time):
        self.tt = time - self.at        # turn-around time(tt)
        self.wt = self.tt - self.bt     # waiting time(wt)
        self.ntt = self.tt / self.bt    # normalized turn-around time
       
    
    
class CPU:
    def __init__(self, process, CPU_type="E"):
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


class RR_readyQueue(readyQueue):
    
    #ready queue기준 도착 시간 우선이라서 필요없을 듯?
    def RR_Priority(self): 
        pass


# 정해진 타임퀀텀만큼 CPU를 할당하고 작업을 완료하지 못하면 ready queue의 맨 뒤에 삽입되어 자기차례를 기다림
class RR:
    
    def __init__(self, process_input, CPU_input):
        self.process = process_input    # process_input 값을 RR클래스의 process로 설정
        self.CPU = CPU_input            # CPU_input 값을 RR클래스의 CPU로 설정
        self.readyQueue = RR_readyQueue()   # RR_readyQueue() 함수를 RR클래스의 readyQueue 변수로 설정

        self.time = 0               # 시간 기준 : 0부터 시작

    def ready_state_RR(self):
        self.readyQueue.enqueue(self.process)  # input된 process를 readyQueue에 삽입

        if(self.CPU.CPU_running == False): # 작업 중인 process가 없다면
            #print("통과했니??dd")
            self.running_state_RR()        # RR running 상태로 돌입

    # 스케쥴링 기준이 먼저 도착한 순서임
    def running_state_RR(self): 
        count = 0

        while count is not len(self.process):
            
           # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)): 
                if self.process[i].at != -1 and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].at = -1 # 이미 추가된 프로세스 예외처리
                    print("process %s arrive" %(i+1))
    

            # CPU가 작동중이지 않다면
            if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면
                if self.CPU.CPU_running is False:
                    self.ready_process = self.readyQueue.dequeue() # 대기큐 맨 앞의 process 꺼내기
                
                    if(self.ready_process.bt - self.ready_process.tq > 0): #bt가 tq보다 커서 해당 프로세스의 일이 끝나지 않았으면
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
                                    print("process %s arrive" %(i+1))
                        #print(self.ready_process)
                        print("일이 덜 끝났으므로 다시 대기큐에 들어가")
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
                                    print("process %s arrive" %(i+1))
                        print("process finish, total time : ", self.time)
                        count += 1
                    
                




                # 아직 추가되지 않은 프로세스이거나 도착시간이 현재시간보다 작거나 같을 때
                # if self.process[i].at is not -1 and self.process[i].at <= self.time:
                    
                #     self.readyQueue.enqueue(self.process[i])    # readyqueue에 프로세스 삽입

                #     self.process[i].at = -1 # 이미 추가된 프로세스 예외처리
                #     print("process %s arrive" %(i+1))

                # CPU가 작동중이지 않다면
            



    def terminated_state_RR(self):
        del self.process


if __name__ == "__main__":
    process1 = process(0, 3, 3)
    process2 = process(1, 7, 3)
    process3 = process(3, 2, 3)
    process4 = process(5, 5, 3)
    process5 = process(6, 3, 3)

    process_list = []
    process_list.append(process1)
    process_list.append(process2)
    process_list.append(process3)
    process_list.append(process4)
    process_list.append(process5)
    
    CPU1 = CPU(process_list)
    RR_test = RR(process_list, CPU1)

    RR_test.running_state_RR()