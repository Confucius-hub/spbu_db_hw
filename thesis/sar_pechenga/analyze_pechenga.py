import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle, FancyArrowPatch
from scipy.ndimage import gaussian_filter, binary_opening, binary_closing, binary_dilation, uniform_filter
from scipy import ndimage as ndi

plt.rcParams['font.family']='DejaVu Sans'
BG='#090c12'; PANEL='#111827'

def load(fn): return np.asarray(Image.open(fn).convert('L'), float)

def texture(a, win=9):
    m = uniform_filter(a, win)
    m2 = uniform_filter(a*a, win)
    return np.sqrt(np.clip(m2-m*m,0,None))

def detect(a, land_pct=80, k=1.3, smooth_pct=45):
    """Smooth+dark water/oil-like; rough=land/tundra. Adaptive threshold inside smooth-water."""
    sm = gaussian_filter(a,1.5)
    tex = texture(sm, 11)
    smooth = tex < np.percentile(tex, smooth_pct)         # low texture = water/film/ice
    bright = sm > np.percentile(sm, land_pct)
    # water = smooth AND not bright
    water = smooth & ~bright
    water = binary_closing(binary_opening(water,iterations=2),iterations=3)
    land = ~water
    wv = sm[water]
    if wv.size < 100:
        return land, np.zeros_like(water), 0,0,0
    mu,sigma = wv.mean(), wv.std()
    T = mu - k*sigma
    cand = water & (sm < max(T, np.percentile(wv,8)))     # darkest smooth water = oil-like
    cand = binary_opening(cand,iterations=2)
    cand = binary_closing(cand,iterations=3)
    lbl,n = ndi.label(cand); sizes=ndi.sum(np.ones_like(lbl),lbl,range(1,n+1))
    keep=np.zeros_like(cand)
    for i,s in enumerate(sizes,1):
        if s>a.size*0.0015: keep|=(lbl==i)
    return land, keep, mu, sigma, T

a1=load('pechenga_feb2026_winter_VV.webp'); H1,W1=a1.shape
a2=load('pechenga_aug2025_summer_VV.webp'); H2,W2=a2.shape
land1,cand1,mu1,sd1,T1=detect(a1,land_pct=80,smooth_pct=55)
land2,cand2,mu2,sd2,T2=detect(a2,land_pct=68,smooth_pct=42)
print(f"Feb: mu={mu1:.1f} sd={sd1:.1f} T={T1:.1f} cand={cand1.mean()*100:.2f}%")
print(f"Aug: mu={mu2:.1f} sd={sd2:.1f} T={T2:.1f} cand={cand2.mean()*100:.2f}%")

fig=plt.figure(figsize=(20,15.5),facecolor=BG)
gs=gridspec.GridSpec(2,2,figure=fig,left=0.025,right=0.85,top=0.90,bottom=0.045,wspace=0.04,hspace=0.13)
axA=fig.add_subplot(gs[0,0]);axB=fig.add_subplot(gs[0,1])
axC=fig.add_subplot(gs[1,0]);axD=fig.add_subplot(gs[1,1])
axI=fig.add_axes([0.86,0.045,0.135,0.855])
for ax in [axA,axB,axC,axD,axI]:
    ax.set_facecolor(PANEL);ax.set_xticks([]);ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_edgecolor('#2d3748')

def ar(ax,fx,fy,txt,col,tfx,tfy,W,H):
    ax.add_patch(FancyArrowPatch((tfx*W,tfy*H),(fx*W,fy*H),arrowstyle='-|>',mutation_scale=13,
                color=col,lw=1.7,shrinkA=3,shrinkB=3))
    ax.text(tfx*W,tfy*H,txt,color='w',fontsize=9,ha='center',va='center',fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.28',fc=col,ec='none',alpha=0.93))

axA.imshow(a1,cmap='gray',vmin=0,vmax=np.percentile(a1,99),aspect='equal')
axA.set_title('A · Печенга, 3 фев 2026  [зима]',color='#93c5fd',fontsize=12.5,fontweight='bold',pad=8)
ar(axA,0.12,0.18,'Кольский берег\n(суша)','#16a34a',0.13,0.05,W1,H1)
ar(axA,0.33,0.13,'острова','#22c55e',0.43,0.04,W1,H1)
ar(axA,0.66,0.50,'Открытое Баренцево море\nЛЬДА НЕТ (тёплое течение)','#2563eb',0.78,0.28,W1,H1)
ar(axA,0.42,0.60,'штиль / ветровая\nтень','#f59e0b',0.28,0.80,W1,H1)

axB.imshow(a2,cmap='gray',vmin=0,vmax=np.percentile(a2,99),aspect='equal')
axB.set_title('B · Печенга, авг 2025  [лето]',color='#fbbf24',fontsize=12.5,fontweight='bold',pad=8)
ar(axB,0.55,0.78,'тундра (суша)','#16a34a',0.68,0.93,W2,H2)
ar(axB,0.72,0.22,'мыс / берег','#22c55e',0.86,0.09,W2,H2)
ar(axB,0.20,0.32,'открытая вода','#2563eb',0.07,0.13,W2,H2)
ar(axB,0.32,0.20,'ВЕТРОВАЯ ТЕНЬ\n= двойник нефти!','#ef4444',0.48,0.05,W2,H2)

def overlay(ax,a,land,cand,title):
    ax.imshow(a,cmap='gray',vmin=0,vmax=np.percentile(a,99),aspect='equal')
    ov=np.zeros((*a.shape,4));ov[...,0]=1;ov[...,1]=0.2;ov[...,3]=cand*0.6
    ax.imshow(ov,aspect='equal')
    ax.set_title(title,color='#f87171',fontsize=12,fontweight='bold',pad=8)
overlay(axC,a1,land1,cand1,f'C · Детектор T=μ−1.3σ (зима): отмечено {cand1.mean()*100:.1f}% кадра')
overlay(axD,a2,land2,cand2,f'D · Детектор T=μ−1.3σ (лето): отмечено {cand2.mean()*100:.1f}% кадра')
axC.text(0.5,-0.055,'Однородная тёмная вода → порог почти ничего не выделяет (нет локальных аномалий)',
         transform=axC.transAxes,color='#fca5a5',fontsize=9,ha='center')
axD.text(0.5,-0.055,'Красное = гладкие тёмные пятна (ветровые тени), ОШИБОЧНО принятые за нефть',
         transform=axD.transAxes,color='#fca5a5',fontsize=9,ha='center')

axI.set_xlim(0,1);axI.set_ylim(0,1)
axI.set_title('Вывод',color='w',fontsize=12,fontweight='bold',pad=10)
blocks=[('#60a5fa','ЗИМА (фев 2026)','Баренцево море у Печенги\nНЕ замерзает (тёплое\nНорвежское течение).\n67% кадра — тёмная\nоткрытая вода без льда.'),
        ('#fbbf24','ЛЕТО (авг 2025)','Открытая вода + локальные\nгладкие тёмные пятна =\nветровые тени в заветрии\nмысов (штиль), биоплёнки.'),
        ('#ef4444','ПРОБЛЕМА','Пороговый детектор\nпомечает гладкие тёмные\nзоны как «нефть». Но\nразливов в Печенге НЕТ\n→ ложные срабатывания.'),
        ('#34d399','РЕШЕНИЕ','PD = σ⁰_VV − σ⁰_VH +\nконтекст (DeepLabV3+)\nотсекают двойники. Для\nПеченги класс «лёд» не\nнужен: вода + ветер.')]
y=0.96
for col,head,body in blocks:
    axI.add_patch(Rectangle((0,y-0.205),1,0.19,fc='#0d1424',ec=col,lw=1.3))
    axI.text(0.06,y-0.03,head,color=col,fontsize=9.5,fontweight='bold',va='top')
    axI.text(0.06,y-0.075,body,color='#cbd5e1',fontsize=8,va='top',linespacing=1.4)
    y-=0.23

fig.text(0.44,0.955,'Печенга: «двойники» нефти без аварий — контрольная акватория (Баренцево море)',
         color='w',fontsize=16,fontweight='bold',ha='center')
fig.text(0.44,0.928,'Sentinel-1 IW GRD · VV · 10 м/пикс · разливов не зафиксировано → все тёмные сигнатуры = ложные цели',
         color='#9aa4b2',fontsize=10,ha='center')
fig.text(0.44,0.013,'Превью-снимки (8-бит). Порог T=μ−kσ (k=1.3) на гладкой водной маске (текстурный фильтр). '
         'Калиброванный σ⁰(дБ)/PD требует .SAFE+SNAP. Печенга = ветровые/биогенные двойники (без льда).',
         color='#4b5563',fontsize=8,ha='center',style='italic')
plt.savefig('pechenga_winter_summer_lookalikes.png',dpi=170,facecolor=BG,bbox_inches='tight')
print('DONE')
