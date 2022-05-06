from tkinter import *
import tkinter.ttk as ttk
import main

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
frame_type = LabelFrame(frame_top, text="Scheduling Type")
frame_type.pack(side="left", padx=(2.5, 10))

# Label(frame_type, text="스케줄링 방식 : ").pack(side="left")

s_values = [ "FCFS", "SPN", "SRTN", "HRRN"]
s_type = ttk.Combobox(frame_type, width = 6, height=4, values=s_values)
s_type.set("FCFS")
s_type.pack(side="left" ,padx = 5, pady = 5)

Button(frame_type, text="Run").pack( padx=(5,5), pady=5, side="right")

############ Process Add ###############
frame_pa = LabelFrame(frame_top, text="Process")
frame_pa.pack(side="right")

Button(frame_pa, text="Delete").pack( padx=(5,5), pady=5, side="right")

############ Processor Add ###############
frame_pra = LabelFrame(frame_top, text="Processor")
frame_pra.pack(side="right")

Label(frame_pra, text="Core : ").pack(side="left")
pc_values = [ "P", "E"]
p_core = ttk.Combobox(frame_pra, width = 1, height=2, values=pc_values)
p_core.set("P")

p_core.pack(side="left")
Button(frame_pra, text="Delete").pack( padx=(2.5,5), pady=5, side="right")
Button(frame_pra, text="Add").pack( padx=(5,2.5), pady=5, side="right")

############ Process Option ###############
frame_po = LabelFrame(frame_top, text="Process Input")
frame_po.pack()

Label(frame_po, text="Arrival Time : ").pack(side="left",  padx = (5,0), pady = 5)
at_e = Entry(frame_po, width=4)
at_e.pack(side="left", padx=(5, 5), pady=5)

Label(frame_po, text="Burst Time : ").pack(side="left",  padx = (5,0), pady = 5)
bt_e = Entry(frame_po, width=4)
bt_e.pack(side="left", padx=(5, 5), pady=5)

i=0
def process_add():
    global i
    ptable.insert('', 'end', text=i+1, values=(at_e.get(), bt_e.get()), iid=str(i)+"번")
    i += 1

Button(frame_po, text="Add", command=process_add).pack( padx=(5,5), pady=5, side="right")

############ Process Table ###############
pbl = Label(root, text="process information")
pbl.pack()

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