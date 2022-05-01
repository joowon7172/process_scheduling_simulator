# SRTN (Short Remaining Time Next) v1.1 made by VRICK
# Preemptive
# 1.1 : maxtime 방식 폐기 (현재시간이 BT합계시간 넘어가는 경우 저 혼자 중단됨), SRTN_readyQueue 따로 만듬 (재경이 고마워!)


class readyQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, items):
        self.items.append(items)

    def dequeue(self):
        if not self.isEmpty(): return self.items.pop(0)

    def isEmpty(self):
        if len(self.items) == 0:
            return True
        else:
            return False

    def peek(self):  # 다음 프로세스 미리보기
        if not self.isEmpty():
            return self.items[0]
        else:
            return False


class SPN_readyQueue(readyQueue):
    def Priority(self):  # 버블 정렬을 이용해 bt가 작은 순으로 오름차순 정렬
        if self.isEmpty() is not True:
            for j in range(len(self.items), 0, -1):
                for i in range(0, j - 1):
                    if self.items[i].bt > self.items[i + 1].bt:
                        self.items[i], self.items[i + 1] = self.items[i + 1], self.items[i]
                    elif self.items[i].bt == self.items[i + 1].bt:
                        if self.items[i].at > self.items[i + 1].at:
                            self.items[i], self.items[i + 1] = self.items[i + 1], self.items[i]


class SRTN_readyQueue(SPN_readyQueue):
    pass
                            

class process:
    def __init__(self, at, bt, id):
        self.at = at
        self.bt = bt
        self.id = id
        self.isUsed = False

    def calculate_time(self, time):
        self.tt = time - self.at
        self.wt = self.tt - self.bt
        self.ntt = self.tt / self.bt


class CPU:
    def __init__(self, process, CPU_type="E"):
        self.process = process
        self.CPU_running = False
        self.type = CPU_type
        self.sumofPower = 0

        if self.type == "E":
            self.processing_per_second = 1
            self.powerConsuming_per_second = 1
            self.powerWaiting_per_second = 0.1

        elif self.type == "P":
            self.processing_per_second = 2
            self.powerConsuming_per_second = 3
            self.powerWaiting_per_second = 0.1

    def running_state(self, process):
        self.CPU_running = True
        while self.CPU_running:
            process.bt -= self.processing_per_second
            self.sumofPower += self.powerConsuming_per_second
            print("Running..." + str(process.bt))
            if process.bt == 0 or not self.CPU_running:
                break

        self.CPU_running = False


class FCFS:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.readyQueue = readyQueue()  # FCFS readyQueue
        self.CPU = CPU_input  # FCFS input CPU
        self.type = CPU_input.type  # FCFS input CPU type

    def ready_state_fcfs(self):
        self.readyQueue.enqueue(self.process)  # input된 process를 readyQueue에 삽입
        if (self.CPU.CPU_running == False):  # 작업 중인 process가 없다면
            print("통과했니??dd")
            self.running_state_fcfs()  # FCFS running 상태로 돌입

    def running_state_fcfs(self):
        self.ready_process = self.readyQueue.dequeue()  # 첫 대기 순번인 process 꺼내기
        while (self.ready_process.bt > 0):
            print("ddd")  # burst time = processing size <= 0 이하가 될 때까지
            self.CPU.running_state(self.ready_process)  # process running
        print("burst time end!!?!??!")
        self.terminated_state_fcfs()  # process finish

    def terminated_state_fcfs(self):
        del self.process


class SPN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.CPU = CPU_input  # FCFS input CPU
        self.readyQueue = SPN_readyQueue()
        self.time = 0  # 시간 기준을 잡기 위함

    def running_state_spn(self):
        count = 0

        while count is not len(self.process):
            # 현재시간과 도착시간을 비교하여 삽입
            for i in range(0, len(self.process)):
                if self.process[i].at is not -1 and self.process[i].at <= self.time:
                    self.readyQueue.enqueue(self.process[i])
                    self.process[i].at = -1  # 이미 추가된 프로세스 예외처리
                    print("process %s arrive" % self.process[i].id)

            self.readyQueue.Priority()  # Priority에 맞게 정렬

            # CPU가 작동중이지 않다면
            if self.CPU.CPU_running is False:
                ready_process = self.readyQueue.dequeue()  # 첫 대기 순번인 process 꺼내기
                while ready_process.bt > 0:
                    self.time += 1
                    self.CPU.running_state(ready_process)  # process running

                print("process finish, total time : ", self.time)

        self.terminated_state_spn()  # process finish
        count += 1

    def terminated_state_spn(self):
        del self.process


class SRTN:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.readyQueue = SRTN_readyQueue()
        self.CPU = CPU_input
        self.type = CPU_input.type
        self.time = 0  # 현재 시간 (lapse)
        self.cnt = 0

    def running_state_srtn(self):
        print("\nTest case started. CPU Type is %s." % self.type)
        while self.cnt <= len(self.process):
            for i in self.process:  # 프로세스 목록에 있는 프로세스들을 모두 돌아볼때까지
                if i.at == self.time and not i.isUsed:  # 한 프로세스의 AT가 현재 시간과 같고 한 번도 검사받은(= 완료된) 적이 없다면
                    self.readyQueue.enqueue(i)  # 대기 큐에 집어넣음
                    print("process %s has arrived at time %s." % (i.id, self.time))
                    i.isUsed = True
                    self.readyQueue.Priority()  # 대기 큐 한번 정렬.

            if self.readyQueue.peek():  # 대기 큐가 빈 상태가 아니라면
                if not self.CPU.CPU_running:  # CPU가 돌아가고 있지 않을 시
                    self.readyQueue.Priority()  # 대기 큐 한번 정렬.
                    ready_process = self.readyQueue.dequeue()  # 대기 프로세스는 대기 큐에서 dequeue된 프로세스
                    self.CPU.CPU_running = True  # 프로세스가 작동 중임을 선언.
                    while ready_process.bt > 0:  # BT가 다 소모되지 않았다면
                        if ready_process.bt == 0:  # 해당 프로세스의 BT가 다 소모되면 반복 탈출.
                            break
                        else:
                            if self.CPU.CPU_running:
                                for j in self.process:  # 한창 돌고 있으면 그 사이 들어올 프로세스 선발
                                    if j.at == self.time and not j.isUsed:
                                        self.readyQueue.enqueue(j)  # 대기 큐에 집어넣음
                                        print("process %s has arrived at time %s." % (j.id, self.time))
                                        j.isUsed = True  # 뽑았으니까 일단 플래그 세우기
                                        self.readyQueue.Priority()  # 대기 큐 한번 정렬.

                                        if j.bt < ready_process.bt:  # 새로 도착한 프로세스가 돌아가고 있는 프로세스보다 bt가 작다면 선점.
                                            ready_process.isUsed = False  # 다시 뽑혀야 되므로 검진 플래그 끄기
                                            self.readyQueue.enqueue(ready_process)  # 다시 큐로 들여보냄.
                                            print("process %s preempted. %s has entered instead." % (ready_process.id, j.id))
                                            ready_process = j  # 새로 도착한 프로세스를 준비시킴.

                                        elif j.bt == ready_process.bt:  # bt가 같은 경우 at가 먼저인 걸 (먼저 도착한걸) 우선하여 작업.
                                            if j.at <= ready_process.at:
                                                ready_process.isUsed = False
                                                self.readyQueue.enqueue(ready_process)
                                                print("process %s preempted. %s has entered instead." % (ready_process.id, j.id))
                                                ready_process = j  # 새로 도착한 프로세스를 준비시킴.

                                ready_process.bt -= self.CPU.processing_per_second  # CPU의 작업능률만큼 bt 소모
                                print("Running %s... BT remains %s. Time is %s." % (ready_process.id, str(ready_process.bt), self.time))
                                self.CPU.sumofPower += self.CPU.powerConsuming_per_second  # 소모전력 (어디다 쓰는지 모름)

                            else:
                                self.CPU.sumofPower += self.CPU.powerWaiting_per_second  # 대기전력 (작업을 안 할 동안 소모되는 전력?)

                        self.time += 1  # 한 작업 완수 시마다 시간 초 증가.

                    self.CPU.CPU_running = False  # 작업 종료 시 CPU 플래그 끄기

                    if ready_process.bt == 0 and ready_process not in self.readyQueue.items:  # 작업이 끝난 프로세스의 BT가 0이고 대기 큐에서 완전히 지워졌다면 종료 메시지
                        print("Process %s ended at time %s." % (ready_process.id, self.time))
                        del ready_process
                        self.cnt += 1

            else:  # 작업 중 대기 큐에 아직 도착한 프로세스가 없거나 할 때
                self.time += 1  # 시간만 +1 해줌.
                self.CPU.sumofPower += self.CPU.powerWaiting_per_second  # 대기전력 (작업을 안 할 동안 소모되는 전력?)
                print("No process in ready queue. Time is %s." % self.time)

            if self.cnt == len(self.process):
                print("Test case ended.")
                break


def main():
    process1 = process(0, 3, 1)
    process2 = process(1, 7, 2)
    process3 = process(3, 2, 3)
    process4 = process(5, 5, 4)
    process5 = process(6, 3, 5)

    process6 = process(0, 4, 1)
    process7 = process(6, 4, 2)
    process8 = process(7, 2, 3)
    process9 = process(9, 2, 4)
    process10 = process(15, 4, 5)

    process_list1 = [process1, process2, process3, process4, process5]
    process_list2 = [process6, process7, process8, process9, process10]

    CPU1 = CPU(process_list1)
    CPU2 = CPU(process_list2, "P")
    srtn_test_case1 = SRTN(process_list1, CPU1)
    srtn_test_case1.running_state_srtn()
    srtn_test_case2 = SRTN(process_list2, CPU2)
    srtn_test_case2.running_state_srtn()


main()
