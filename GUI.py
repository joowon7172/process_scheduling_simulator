from tkinter import *
import tkinter.ttk as ttk
import option as op
from FCFS import *
from SPN import *
from RR import *
from SRTN import *
from SPNRR import *
from HRRN import *
from gantt import * 
import matplotlib.pyplot as plt
import tkinter.messagebox as msgbox

root = Tk() # Tk 시작

############ Frame Setting ###############
frame_name = Label(root, text="9팀 : 문승벽, 염승돈, 임재경, 차주원")
frame_name.pack(anchor=NW)

############ Frame Seperator #############
s = ttk.Separator(root, orient="horizontal")
s.pack(fill='x')

# 제목 설정
root.title("Process Scheduling Simulator")

# 창 크기 지정
root.geometry("1000x500+0+0")

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

############ time quantum input ############
def clear(event):       # 좌클릭 할 시 입력값이 사라지는 함수
    tq_e.delete(0, len(tq_e.get()))     # 입력값이 사라짐

tq_e = Entry(frame_type)
tq_e.bind("<Button-1>", clear)  # 좌클릭 할 시 라벨 사라짐

############ Time Quantum 조건 ##############
def call_Tq_Func(event):        # time quantum 입력창 나오게 하는 함수
    if s_type.get() == "RR" or s_type.get() == "SPNRR":     # RR or SPNRR 인 경우
        tq_e.pack(pady=(9, 0))          # tq 입력창 나타나기
        tq_e.insert(0, "time quantum")
    else:                               # 다른 스케줄링 기법인 경우
        tq_e.pack_forget()              # tq 입력창 사라지기

############ Scheduling Type Setting ##############
s_values = [ "FCFS", "RR", "SPN", "SRTN", "HRRN", "SPNRR"]
s_type = ttk.Combobox(frame_type, width = 6, height=6, values=s_values)
s_type.set("FCFS")
s_type.pack(side="left" ,padx = 5, pady = 5)
s_type.bind("<<ComboboxSelected>>", call_Tq_Func)

############ RUN BUTTON FUNCTION ##############
def run():      # 실행 버튼을 눌렀을 때
    global plist, cpu1, label_photo, power
    type = s_type.get()     # type은 스케줄링 타입

    if type == "FCFS":      # FCFS일 때
        fcfs = FCFS(plist, cpu1)
        fcfs.running()
        power = Label(root, text= "Power Consuming : "+str(cpu1.sumofPower))
        power.pack()    
        for i in range(0, len(plist)):
            ptable.item(str(i)+"번", text=i+1, values=(plist[i].tmp_at, plist[i].tmp_bt, plist[i].wt, plist[i].tt, plist[i].ntt))  
        fcfs.gantt.show_gantt("FCFS Scheduling Gantt", fcfs.time)   
        
    if type == "RR":       # RR일 때
        rr = RR(plist, cpu1, int(tq_e.get()))
        rr.running()
        power = Label(root, text= "Power Consuming : "+str(cpu1.sumofPower))
        power.pack()    
        for i in range(0, len(plist)):
            ptable.item(str(i)+"번", text=i+1, values=(plist[i].tmp_at, plist[i].tmp_bt, plist[i].wt, plist[i].tt, plist[i].ntt))
        rr.gantt.show_gantt("RR Scheduling Gantt", rr.time)    

    if type == "SPN":       # SPN일 때
        spn = SPN(plist, cpu1)
        spn.running()
        power = Label(root, text= "Power Consuming : "+str(cpu1.sumofPower))
        power.pack()    
        for i in range(0, len(plist)):
            ptable.item(str(i)+"번", text=i+1, values=(plist[i].tmp_at, plist[i].tmp_bt, plist[i].wt, plist[i].tt, plist[i].ntt))
        spn.gantt.show_gantt("SPN Scheduling Gantt", spn.time)

    if type == "SRTN":      # SRTN일 때
        srtn = SRTN(plist, cpu1)
        srtn.running()
        power = Label(root, text= "Power Consuming : "+str(cpu1.sumofPower))
        power.pack()
        for i in range(0, len(plist)):
            ptable.item(str(i)+"번", text=i+1, values=(plist[i].tmp_at, plist[i].tmp_bt, plist[i].wt, plist[i].tt, plist[i].ntt))
        srtn.gantt.show_gantt("SRTN Scheduling Gantt", srtn.time)

    if type == "HRRN":      # HRRN일 때
        hrrn = HRRN(plist, cpu1)
        hrrn.running()
        power = Label(root, text= "Power Consuming : "+str(cpu1.sumofPower))
        power.pack()
        for i in range(0, len(plist)):
            ptable.item(str(i)+"번", text=i+1, values=(plist[i].tmp_at, plist[i].tmp_bt, plist[i].wt, plist[i].tt, plist[i].ntt))
        hrrn.gantt.show_gantt("HRRN Scheduling Gantt", hrrn.time)

    if type == "SPNRR":    # SPNRR일 때
        spnrr = SPNRR(plist, cpu1, int(tq_e.get()))
        spnrr.running()
        power = Label(root, text= "Power Consuming : "+str(cpu1.sumofPower))
        power.pack()
        for i in range(0, len(plist)):
            ptable.item(str(i)+"번", text=i+1, values=(plist[i].tmp_at, plist[i].tmp_bt, plist[i].wt, plist[i].tt, plist[i].ntt))
        spnrr.gantt.show_gantt("SPNRR Scheduling Gantt", spnrr.time)

Button(frame_type, text="Run", command=run).pack( padx=(5,5), pady=5, side="right")

############ Process Option ###############
frame_po = LabelFrame(frame_top, text="Process Input")
frame_po.pack(side="left")

############ Arrival Time Entry ###########
Label(frame_po, text="Arrival Time : ").pack(side="left",  padx = (5,0), pady = 5)
at_e = Entry(frame_po, width=4)
at_e.pack(side="left", padx=(5, 5), pady=5)

############ Burst Time Entry ###########
Label(frame_po, text="Burst Time : ").pack(side="left",  padx = (5,0), pady = 5)
bt_e = Entry(frame_po, width=4)
bt_e.pack(side="left", padx=(5, 5), pady=5)

############ Process Input Setting #############
i=0
id = 1
plist = []

########### Process Add Function ###############
def process_add():
    global i, id, plist
    p = op.process(int(at_e.get()), int(bt_e.get()), i+1)
    plist.append(p)
    ptable.insert('', 'end', text=i+1, values=(at_e.get(), bt_e.get()), iid=str(i)+"번")
    i += 1
    if(i == 15) :
        msgbox.showwarning("Warning", "프로세스 개수는 최대 15개입니다.")
        padd_btn['state'] = DISABLED   
        
padd_btn = Button(frame_po, text="Add", command=process_add)
padd_btn.pack( padx=(5,5), pady=5, side="right")

############ Process delete ###############
frame_pa = LabelFrame(frame_top, text="Process")
frame_pa.pack(side="left")

def process_del():      # 프로세스 삭제 버튼 누를 시 이벤트
    global i, power            # 전역변수 i
    
    if i > 0:
        i -= 1
        ptable.delete(str(i)+"번")
        plist.pop()
        padd_btn.config(state=NORMAL)
        power.pack_forget()
        cpu1.sumofPower = 0
        

Button(frame_pa, text="Delete", command=process_del).pack( padx=(5,5), pady=5, side="left")

############ Process reset ###############
def process_reset():      # 프로세스 삭제 버튼 누를 시 이벤트
    global i                # 전역변수 i
    
    while i > 0: 
        i -= 1
        ptable.delete(str(i)+"번")
        plist.pop()
        padd_btn.config(state=NORMAL)
        power.pack_forget()
        cpu1.sumofPower = 0

Button(frame_pa, text="Reset", command=process_reset).pack( padx=(5,5), pady=5, side="right")

############ Processor Interface ###############
frame_pra = LabelFrame(frame_top, text="Processor")
frame_pra.pack(side="right")

Label(frame_pra, text="Core : ").pack(side="left")

pc_values = ["E", "P"]
p_core = ttk.Combobox(frame_pra, width = 1, height=2, values=pc_values)
p_core.set("E")
cpu_msg = Label(root, text=" ")
cpu_msg.pack()
s2 = ttk.Separator(root, orient="horizontal")
s2.pack(fill='x')

cpu1 = 0

############# Processor Add Function ##########
def cpu_add():
    global plist
    global cpu1

    if p_core.get() == "E":
        cpu1 = op.CPU(plist, "E")
        cpu_msg.config(text="cpu type E is generated.")
    elif p_core.get() == "P":
        cpu1 = op.CPU(plist, "P")
        cpu_msg.config(text="cpu type P is generated.")

############ Processor Delete Function ###########
def cpu_del():
    global cpu1 

    del cpu1

    if p_core.get() == "E":
        cpu_msg.config(text="cpu type E is deleted.")
    elif p_core.get() == "P":
        cpu_msg.config(text="cpu type P is deleted.")

p_core.pack(side="left")
Button(frame_pra, text="Delete", command=cpu_del).pack( padx=(2.5,5), pady=5, side="right")
Button(frame_pra, text="Add", command=cpu_add).pack( padx=(5,2.5), pady=5, side="right")

############ Process Table ###############
ptbl = Label(root, text="Process information")
ptbl.pack(anchor="center")

# 표 생성하기.
ptable = ttk.Treeview(root, height=15, columns=["one", "two", "three", "four", "five"])
ptable.pack(anchor="s")

ptable.column("#0", width=50)
ptable.heading("#0", text="id")

ptable.column("#1", width=120, anchor="center")
ptable.heading("one", text="Arrival Time", anchor="center")

ptable.column("#2", width=120, anchor="center")
ptable.heading("two", text="Burst Time", anchor="center")

ptable.column("#3", width=150, anchor="center")
ptable.heading("three", text="Waiting Time", anchor="center")

ptable.column("#4", width=150, anchor="center")
ptable.heading("four", text="Turn-around Time", anchor="center")

ptable.column("#5", width=200, anchor="center")
ptable.heading("five", text="Normalized Turn-around Time", anchor="center")

############## Program Exit ####################
def exit():
    if msgbox.askokcancel("종료", "종료하시겠습니까?"):
        print("종료")
        root.destroy()

root.protocol('WM_DELETE_WINDOW', exit)

root.mainloop()