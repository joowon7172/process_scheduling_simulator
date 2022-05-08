import matplotlib.pyplot as plt
import numpy as np
import random
import datetime

class Gantt:  # 차트
    def __init__(self, process_num):
        self.gantt_list = []
        self.process_num = process_num
        plt.rc('font', size=20)
        plt.rc('axes', titlesize=12)     # fontsize of the axes title
        plt.rc('xtick', labelsize=10)    # fontsize of the tick labels
        plt.rc('ytick', labelsize=0)    # fontsize of the tick labels


    def store(self, t1, t2, t3):  # 프로세스 정보 저장
        self.gantt_list.append((t1, t2, t3))

    def show_gantt(self, method, time):
        fig, gnt = plt.subplots(1, figsize=(time, 3)) # x,y 길이 set
        plt.suptitle(method)
        
        # 축 value set
        gnt.set_ylim(0, 1)
        gnt.set_xlim(0, time)

        xticklabel = []  # x축 틱 제목
        xticks = []   # x축 틱

        for timeindex in range(time+1):  # 시간 하나마다 인덱스 설정.
            xticks.append(timeindex)  # 각 빈 리스트에 인덱스 저장.
            xticklabel.append(timeindex)

        # 저장한 각 인덱스 x축에 적용.
        gnt.set_xticks(xticks)
        gnt.set_xticklabels(xticklabel)

        gnt.grid(False)  # 그리드 설정(해제)
        color = []

        for j in range(self.process_num):  # 같은 ID의 프로세스는 같은 색으로 표현하기 위해 각 ID마다 고유한 랜덤 색 할당
            color.append((np.random.random(), np.random.random(), np.random.random()))  # 각 간트 바의 색을 랜덤하게 출력.

        for i in self.gantt_list:
            gnt.broken_barh([(i[0], i[1] - i[0])], (0, 1), facecolors=color[i[2] - 1])  # 간트 바 출력 ([x좌표, 길이], (y좌표, 높이), 색(color 리스트의 id번째 배열))
            gnt.text((i[0] + i[1])/2 , 0.5, "P" + str(i[2]), va='center', ha='center', alpha=0.8)  # 간트 바 텍스트 설정 (각 프로세스 ID 출력)


        now = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = str(now) + str(random.randint(0, 500)) + 'gantt.png'  # 파일명 설정 (날짜 + 랜덤한 수 + gantt.png)
        plt.savefig(filename)  # 파일명대로 간트 차트 이미지파일 png로 내보내기.

        plt.show()
        