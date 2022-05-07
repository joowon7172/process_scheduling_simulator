from tkinter import *
import tkinter.ttk as ttk
import main
import option as op
#import FCFS
import SPN
from HRRN import *
import SRTN
#import RR
#import SPNRR

root = Tk()
############ Frame Setting ###############

# 제목 설정
root.title("Process Scheduling Simulator")

# 창 크기 지정
# root.geometry("640x480")

# 창 너비, 높이 조정 불가
root.resizable(False, False)

############ Frame Setting ###############
frame_top = Frame(root, width=640)
frame_top.pack(anchor=N)

frame_mid = Frame(root)
frame_mid.pack(anchor=CENTER)


############ Scheduling Type Setting ##############
frame_type = LabelFrame(frame_top, text="Scheduling Type", height="50")
frame_type.pack(side="left", padx=(2.5, 10))

# Label(frame_type, text="스케줄링 방식 : ").pack(side="left")

############ time quantum input ############

def clear(event):       # 좌클릭 할 시 입력값이 사라지는 함수
    tq_e.delete(0, len(tq_e.get()))     # 입력값이 사라짐

tq_e = Entry(frame_type)
tq_e.bind("<Button-1>", clear)  # 좌클릭 할 시 라벨 사라짐
#############################################

def call_Tq_Func(event):        # time quantum 입력창 나오게 하는 함수
    if s_type.get() == "RR" or s_type.get() == "SPNRR":     # RR or SPNRR 인 경우
        tq_e.pack(pady=(9, 0))          # tq 입력창 나타나기
        tq_e.insert(0, "time quantum")
    else:                               # 다른 스케줄링 기법인 경우
        tq_e.pack_forget()              # tq 입력창 사라지기

s_values = [ "FCFS", "RR", "SPN", "SRTN", "HRRN", "SPNRR"]
s_type = ttk.Combobox(frame_type, width = 6, height=6, values=s_values)
s_type.set("FCFS")
s_type.pack(side="left" ,padx = 5, pady = 5)
s_type.bind("<<ComboboxSelected>>", call_Tq_Func)

def run():      # 실행 버튼을 눌렀을 때
    global plist, i
    type = s_type.get()     # type은 스케줄링 타입

    #if type == "FCFS":      # FCFS일 때
    #    fcfs = FCFS()
    #    fcfs.running   
    #if type == "RR":       # RR일 때
    #    rr = RR()
    if type == "SPN":       # SPN일 때
        spn = SPN()
        spn.running
    if type == "SRTN":      # SRTN일 때
        srtn = SRTN()
        srtn.running
    if type == "HRRN":      # HRRN일 때
        hrrn = HRRN(plist, op.CPU(plist))
        hrrn.running()
        #ptable.insert('', 'end', text=i+1, values=(at_e.get(), bt_e.get()), iid=str(i)+"번")
    #if type == "SPNRR":    # SPNRR일 때
    #    spnrr = SPNRR()

Button(frame_type, text="Run", command=run).pack( padx=(5,5), pady=5, side="right")

############ Process Option ###############
frame_po = LabelFrame(frame_top, text="Process Input")
frame_po.pack(side="left")

Label(frame_po, text="Arrival Time : ").pack(side="left",  padx = (5,0), pady = 5)
at_e = Entry(frame_po, width=4)
at_e.pack(side="left", padx=(5, 5), pady=5)

Label(frame_po, text="Burst Time : ").pack(side="left",  padx = (5,0), pady = 5)
bt_e = Entry(frame_po, width=4)
bt_e.pack(side="left", padx=(5, 5), pady=5)

i=0
id = 1
plist = []
def process_add():
    global i, id, plist
    plist.append(op.process(at_e.get(), bt_e.get(), i+1))
    ptable.insert('', '2', text=i+1, values=(at_e.get(), bt_e.get()), iid=str(i)+"번")
    i += 1

Button(frame_po, text="Add", command=process_add).pack( padx=(5,5), pady=5, side="right")

############ Process delete ###############
frame_pa = LabelFrame(frame_top, text="Process")
frame_pa.pack(side="left")

def process_del():      # 프로세스 삭제 버튼 누를 시 이벤트
    global i            # 전역변수 i
    ptable.delete(iid=str(i))   # iid 값을 가지는 항목 삭제
    # 해당하는 프로세스.__del__

Button(frame_pa, text="Delete", command=process_del).pack( padx=(5,5), pady=5, side="right")

############ Processor Add ###############
frame_pra = LabelFrame(frame_top, text="Processor")
frame_pra.pack(side="right")

Label(frame_pra, text="Core : ").pack(side="left")
pc_values = [ "P", "E"]
p_core = ttk.Combobox(frame_pra, width = 1, height=2, values=pc_values)
p_core.set("P")

def cpu_add():
    global plist
    cpu1 = op.CPU(plist)

p_core.pack(side="left")
Button(frame_pra, text="Delete").pack( padx=(2.5,5), pady=5, side="right")
Button(frame_pra, text="Add", command=cpu_add).pack( padx=(5,2.5), pady=5, side="right")

############ Process Table ###############
ptbl = Label(root, text="Process information")
ptbl.pack()

# 표 생성하기.
ptable = ttk.Treeview(root, columns=["one", "two", "three", "four", "five"])
ptable.pack()

ptable.column("#0", width=50)
ptable.heading("#0", text="id")

ptable.column("#1", width=120, anchor="center")
ptable.heading("one", text="Arrival Time", anchor="center")

ptable.column("#2", width=120, anchor="center")
ptable.heading("two", text="Burst Time", anchor="center")

ptable.column("#3", width=150, anchor="center")
ptable.heading("three", text="Wating Time", anchor="center")

ptable.column("#4", width=150, anchor="center")
ptable.heading("four", text="Turn-around Time", anchor="center")

ptable.column("#5", width=200, anchor="center")
ptable.heading("five", text="Normalized Turn-around Time", anchor="center")

root.mainloop()