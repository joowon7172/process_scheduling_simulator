import option as op
import SPN
import HRRN
import SRTN

if __name__ == "__main__":
    process1 = op.process(0, 3, 1)
    process2 = op.process(1, 7, 2)
    process3 = op.process(3, 2, 3)
    process4 = op.process(5, 5, 4)
    process5 = op.process(6, 3, 5)

    process_list = []
    process_list.append(process1)
    process_list.append(process2)
    process_list.append(process3)
    process_list.append(process4)
    process_list.append(process5)
    
    CPU1 = op.CPU(process_list)
    #spn = SPN.SPN(process_list, CPU1)
    hrrn = HRRN.HRRN(process_list, CPU1)
    #srtn = SRTN.SRTN(process_list, CPU1)
    
    #spn.running()
    #srtn.running()
    hrrn.running()
    
    
