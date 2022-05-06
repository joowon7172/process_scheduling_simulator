import matplotlib.pyplot as plt
import numpy as np
import random
import datetime

class Gantt:  # 차트
    def __init__(self):
        self.gantt_list = []

    def store(self, t1, t2, t3):  # 프로세스 정보 저장
        self.gantt_list.append((t1, t2, t3))

    def show_gantt(self, method):

        fig, gnt = plt.subplots()
        plt.suptitle(method)

        gnt.set_ylim(0, 10)
        gnt.set_xlim(0, 20)

        gnt.set_xlabel('timelapse since start')  # x축 제목 인덱스
        xticklabel = []  # x축 틱 제목
        xticks = []   # x축 틱

        for timeindex in range(21):  # 시간 하나마다 인덱스 설정.
            xticks.append(timeindex)  # 각 빈 리스트에 인덱스 저장.
            xticklabel.append(timeindex)

        # 저장한 각 인덱스 x축에 적용.
        gnt.set_xticks(xticks)
        gnt.set_xticklabels(xticklabel)

        gnt.grid(False)  # 그리드 설정(해제)

        for i in self.gantt_list:
            color = (np.random.random(), np.random.random(), np.random.random())  # 각 간트 바의 색을 랜덤하게 추력.
            gnt.broken_barh([(i[0], i[1] - i[0])], (i[2], 1), facecolors=color)  # 간트 바 출력 ([x좌표, 길이], (y좌표, 높이), 색)
            gnt.text(i[1] + 0.5, i[2] + 0.5, i[2], va='center', ha='right', alpha=0.8)  # 간트 바 텍스트 설정 (각 프로세스 ID 출력)

        now = datetime.datetime.now().strftime('%Y-%m-%d')
        filename = str(now) + str(random.randint(0, 500)) + 'gantt.png'  # 파일명 설정 (날짜 + 랜덤한 수 + gantt.png)
        plt.savefig(filename)  # 파일명대로 간트 차트 이미지파일 png로 내보내기.
        plt.show()  # 간트 차트 창 띄움.
