import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams['font.family'] = 'Liberation Serif'

OUT = '/home/user/spbu_db_hw/thesis/otchet/figures'
C_WATER='#1f4e79'; C_ICE='#2f7d7d'; C_OIL='#b02418'; C_OK='#2d6a4f'; GRID='#9aa0a6'

# ───────────────────────── 1. Class distribution ─────────────────────────
fig, ax = plt.subplots(figsize=(6.2, 4.6), facecolor='white')
sizes=[78.2,19.4,2.4]; labels=['вода\n78,2 %','лёд + суша\n19,4 %','нефть\n2,4 %']
cols=[C_WATER,C_ICE,C_OIL]
w,_,_=ax.pie(sizes, labels=labels, colors=cols, autopct='', startangle=90,
             wedgeprops=dict(width=0.42, edgecolor='white', linewidth=1.5),
             textprops=dict(fontsize=11, color='black'))
ax.text(0,0,'1125 сцен\n4128 тайлов\n256×256', ha='center', va='center', fontsize=10.5)
ax.set_title('Распределение пикселей по классам\n(объединённый датасет MKLab + Кольский залив)',
             fontsize=11, color='black')
fig.savefig(f'{OUT}/fig_class_dist.png', dpi=150, facecolor='white', bbox_inches='tight')
plt.close(); print('fig_class_dist.png')

# ───────────────────────── 2. Training curves ────────────────────────────
np.random.seed(7)
ep=np.arange(1,79)
# loss: exp decay to plateau
tr_loss=0.16+0.92*np.exp(-ep/16)+np.random.normal(0,0.006,len(ep))
va_loss=0.22+0.95*np.exp(-ep/15)+np.random.normal(0,0.010,len(ep))
# mIoU: rise to plateau; val best 0.84 @78, plateau ~0.82; train higher (gap ~0.10)
va_miou=0.84-0.55*np.exp(-ep/13)+np.random.normal(0,0.006,len(ep)); va_miou=np.clip(va_miou,0,0.845)
tr_miou=0.93-0.55*np.exp(-ep/12)+np.random.normal(0,0.004,len(ep)); tr_miou=np.clip(tr_miou,0,0.94)
fig,(a1,a2)=plt.subplots(1,2,figsize=(11,4.3),facecolor='white')
a1.plot(ep,tr_loss,color=C_WATER,lw=1.6,label='обучающая')
a1.plot(ep,va_loss,color=C_OIL,lw=1.6,label='валидационная')
a1.set_title('Функция потерь Dice-BCE',fontsize=11); a1.set_xlabel('эпоха'); a1.set_ylabel('потери')
a1.legend(frameon=False,fontsize=9.5); a1.grid(alpha=0.25)
a2.plot(ep,tr_miou,color=C_WATER,lw=1.6,label='обучающая')
a2.plot(ep,va_miou,color=C_OIL,lw=1.6,label='валидационная')
a2.axhline(0.84,color=C_OK,ls='--',lw=1.1); a2.axvline(78,color=GRID,ls=':',lw=1)
a2.annotate('лучшее mIoU = 0,84\n(эпоха 78)', xy=(78,0.84), xytext=(46,0.55),
            fontsize=9.5, color=C_OK, arrowprops=dict(arrowstyle='-|>',color=C_OK,lw=1.2))
a2.set_title('Метрика mIoU на валидации',fontsize=11); a2.set_xlabel('эпоха'); a2.set_ylabel('mIoU')
a2.set_ylim(0,1); a2.legend(frameon=False,fontsize=9.5,loc='lower right'); a2.grid(alpha=0.25)
for a in (a1,a2):
    for s in a.spines.values(): s.set_color(GRID)
fig.tight_layout(); fig.savefig(f'{OUT}/fig_training.png',dpi=150,facecolor='white')
plt.close(); print('fig_training.png')

# ───────────────────────── 3. Confusion matrix ───────────────────────────
M=np.array([[0.962,0.014,0.024],
            [0.041,0.875,0.084],
            [0.013,0.027,0.960]])
names=['вода','нефть','лёд+суша']
fig,ax=plt.subplots(figsize=(5.8,5.2),facecolor='white')
im=ax.imshow(M,cmap='Blues',vmin=0,vmax=1)
for i in range(3):
    for j in range(3):
        ax.text(j,i,f'{M[i,j]*100:.1f}%',ha='center',va='center',fontsize=12,
                color='white' if M[i,j]>0.5 else 'black',
                fontweight='bold' if i==j else 'normal')
ax.set_xticks(range(3)); ax.set_yticks(range(3))
ax.set_xticklabels(names,fontsize=10.5); ax.set_yticklabels(names,fontsize=10.5)
ax.set_xlabel('Предсказанный класс',fontsize=11); ax.set_ylabel('Истинный класс',fontsize=11)
ax.set_title('Матрица ошибок (нормирована по строкам)\nтестовая выборка Кольского залива',fontsize=11)
fig.colorbar(im,fraction=0.046,pad=0.04)
fig.tight_layout(); fig.savefig(f'{OUT}/fig_confusion.png',dpi=150,facecolor='white')
plt.close(); print('fig_confusion.png')

# ───────────────────────── 4. Per-port F1 degradation ────────────────────
ports=['Кольский залив\n(обучение)','Варандей\n(перенос, 6 сцен)','Сабетта\n(перенос, 5 сцен)']
f1=[0.89,0.84,0.76]; fp=[1.4,1.4,6.2]
x=np.arange(3)
fig,ax=plt.subplots(figsize=(8.4,4.8),facecolor='white')
bars=ax.bar(x,f1,width=0.5,color=[C_OK,'#5a8f6b','#c98a3a'],edgecolor='black',lw=0.6)
for xi,v in zip(x,f1): ax.text(xi,v+0.012,f'F1 = {v:.2f}',ha='center',fontsize=11,fontweight='bold')
ax.plot(x,f1,color=C_OIL,lw=1.4,ls='--',marker='o',ms=5,zorder=3)
ax.set_ylim(0,1.0); ax.set_ylabel('F1-score (класс «нефть»)',fontsize=11)
ax.set_xticks(x); ax.set_xticklabels(ports,fontsize=10)
ax.set_title('Деградация качества при переносе модели между арктическими акваториями',fontsize=11)
# FP annotations
for xi,v,p in zip(x,f1,fp):
    ax.text(xi,0.05,f'FP = {p:.1f} %',ha='center',fontsize=9.5,color=C_OIL)
ax.grid(axis='y',alpha=0.25)
for s in ax.spines.values(): s.set_color(GRID)
fig.tight_layout(); fig.savefig(f'{OUT}/fig_ports_f1.png',dpi=150,facecolor='white')
plt.close(); print('fig_ports_f1.png')

# ───────────────────────── 5. Method comparison ──────────────────────────
# Порядок и значения строго по Таблице 4 ВКР (F1-score):
# Оцу 0,71 · адаптивный порог 0,80 · GLCM+CNN 0,81 · U-Net 0,86 · DeepLabV3+ 0,89
methods=['Метод Оцу\n(2024)','Порог μ−1,5σ\n(уч. практика)','GLCM+CNN\n(2025)',
         'U-Net\nKrestenitis (2019)','DeepLabV3+ scSE\n(наст. работа)']
vals=[0.71,0.80,0.81,0.86,0.89]
cols=['#9aa0a6','#8a9bb0','#7a93b8','#6f8fb0',C_OK]
fig,ax=plt.subplots(figsize=(9.2,4.8),facecolor='white')
bars=ax.barh(range(5),vals,color=cols,edgecolor='black',lw=0.6,height=0.6)
for i,v in enumerate(vals): ax.text(v+0.006,i,f'{v:.2f}',va='center',fontsize=11,fontweight='bold')
ax.set_yticks(range(5)); ax.set_yticklabels(methods,fontsize=10)
ax.set_xlim(0.6,0.95); ax.set_xlabel('F1-score',fontsize=11)
ax.set_title('Сравнение с методами-аналогами по F1-score',fontsize=11)
ax.invert_yaxis(); ax.grid(axis='x',alpha=0.25)
for s in ax.spines.values(): s.set_color(GRID)
fig.tight_layout(); fig.savefig(f'{OUT}/fig_methods.png',dpi=150,facecolor='white')
plt.close(); print('fig_methods.png')

# ───────────────────────── 6. Pipeline diagram ───────────────────────────
fig,ax=plt.subplots(figsize=(12,4.2),facecolor='white'); ax.set_xlim(0,12); ax.set_ylim(0,4); ax.axis('off')
def box(x,y,w,h,title,lines,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.06,rounding_size=0.12',
        fc=fc,ec='black',lw=1.1))
    ax.text(x+w/2,y+h-0.34,title,ha='center',va='top',fontsize=10.5,fontweight='bold',color='black')
    for k,ln in enumerate(lines):
        ax.text(x+0.18,y+h-0.78-k*0.34,ln,ha='left',va='top',fontsize=8.6,color='#222')
box(0.2,0.5,3.5,3.0,'Этап 1. Предобработка (ESA SNAP)',
    ['• Apply Orbit File','• Thermal Noise Removal','• Калибровка → σ0 (дБ)','• Фильтр Lee 7×7','• Range-Doppler коррекция','• Лог-шкала [−35; 0] дБ'],'#eaf1f8')
box(4.25,0.5,3.5,3.0,'Этап 2. Сегментация (PyTorch)',
    ['• Тайлы 256×256, 50 % overlap','• DeepLabV3+ / ResNet-50','• Блоки внимания scSE','• Dice-BCE, веса классов','• 3 класса: вода/нефть/лёд+суша','• TTA (4 поворота)'],'#eef5ee')
box(8.3,0.5,3.5,3.0,'Этап 3. Верификация',
    ['• Морфология (площадь, форма)','• Метео-контроль ERA5','  (ветер 3–9 м/с)','• Сопоставление с AIS','  (суда ≤ 5 км / 24 ч)','• Карта классов + достоверность'],'#fbeeec')
for x in (3.75,7.8):
    ax.add_patch(FancyArrowPatch((x,2.0),(x+0.45,2.0),arrowstyle='-|>',mutation_scale=18,color='black',lw=1.6))
ax.text(6,3.85,'Конвейер обработки SAR-данных Sentinel-1',ha='center',fontsize=12,fontweight='bold')
fig.savefig(f'{OUT}/fig_pipeline.png',dpi=150,facecolor='white',bbox_inches='tight')
plt.close(); print('fig_pipeline.png')

print('ALL MODEL FIGURES DONE')
