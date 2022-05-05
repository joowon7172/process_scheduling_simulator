import option as op

class FCFS:
    def __init__(self, process_input, CPU_input):
        self.process = process_input
        self.readyQueue = op.readyQueue()               # FCFS readyQueue
        self.CPU = CPU_input                      # FCFS input CPU
        self.type = CPU_input.type                # FCFS input CPU type
        self.time = 0
        self.cnt = 0

        print("\nTest case started. CPU Type is %s." % self.type)

    def running(self):
        while self.cnt <= len(self.process):
            for i in self.process:
                if i.at is not -1 and i.at <= self.time:
                    self.readyQueue.enqueue(i)
                    print("process %d arrive at time %s" % (i.id, self.time))
                    i.at = -1

        if self.cnt == len(self.process):
            print("Test case ended.")
            break
            
        if self.readyQueue.peek():
            if self.CPU.CPU_running is False:
                self.ready_process = self.readyQueue.dequeue()  

                for i in self.process:
                    if i.at is not -1 and i.at <= self.time:
                        self.readyQueue.enqueue(i)
                        print("process %d arrive at time %s." % (i.id, self.time))
                        i.at = -1

        self.cnt += 1

    def running_state_fcfs(self):
        self.ready_process = self.readyQueue.dequeue() # 첫 대기 순번인 process 꺼내기
        while(self.ready_process.bt > 0):
            print("ddd")                   # burst time = processing size <= 0 이하가 될 때까지
            self.CPU.running_state(self.ready_process) # process running
        print("burst time end!!?!??!")
        self.terminated_state_fcfs()                        # process finish

    def terminated_state_fcfs(self):
        del self.process