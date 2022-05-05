import copy

import option as op
import FCFS
import SPN
import HRRN
import SRTN


if __name__ == "__main__":

    process_num = int(input("Number of Processes: "))
    process_list = []

    for i in range(0, process_num):
        at = int(input("AT of Process %d: " % (i + 1)))
        bt = int(input("BT of Process %d: " % (i + 1)))
        process = op.process(at, bt, i + 1)
        process_list.append(process)

    processor_num = int(input("Number of Processors: "))
    processor_list = []

    for j in range(0, processor_num):
        type = input("Processor %d Type (E / P) : " % (j + 1))
        CPU = op.CPU(process_list, type)
        processor_list.append(CPU)

    case_num = int(input("Number of Cases: "))

    for k in range(0, case_num):
        case_list = copy.deepcopy(process_list)
        print("1: FCFS 2: SPN 3: SRTN 4: HRRN")
        opt = int(input("Algotithm : "))
        CPU_id = int(input("CPU ID : "))
        if opt == 1:
            fcfs = FCFS.FCFS(case_list, processor_list[CPU_id - 1])
            fcfs.running_state_fcfs()
        elif opt == 2:
            spn = SPN.SPN(case_list, processor_list[CPU_id - 1])
            spn.running()
        elif opt == 3:
            srtn = SRTN.SRTN(case_list, processor_list[CPU_id - 1])
            srtn.running()
        elif opt == 4:
            hrrn = HRRN.HRRN(case_list, processor_list[CPU_id - 1])
            hrrn.running()
