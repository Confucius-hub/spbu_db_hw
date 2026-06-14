"""Shared light-academic styling for thesis SAR figures (Times-New-Roman-like)."""
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from scipy import ndimage as ndi
from scipy.ndimage import gaussian_filter, binary_opening, binary_closing, uniform_filter

# Liberation Serif is metrically identical to Times New Roman
plt.rcParams['font.family'] = 'Liberation Serif'
plt.rcParams['mathtext.fontset'] = 'dejavuserif'

# Academic palette (muted, print-safe)
COL = {
    'water':  '#1f4e79',   # dark blue — water / sea
    'oil':    '#b02418',   # dark red — oil / anomaly / look-alike
    'land':   '#7a5c1e',   # ochre — tundra / land
    'ice':    '#2f7d7d',   # teal — ice
    'iceL':   '#5fa8a8',   # light teal — drift / young ice
    'coast':  '#555555',   # gray — coastline
    'veg':    '#2d6a4f',   # dark green — vegetation
    'infra':  '#b8860b',   # dark goldenrod — port infrastructure
    'sky':    '#356ab3',   # medium blue
}
FACE = 'white'
GRID = '#9aa0a6'

def load(path):
    return np.asarray(Image.open(path).convert('L'), float)

def load_rgb(path):
    return np.asarray(Image.open(path).convert('RGB'))

def texture(a, win=9):
    m = uniform_filter(a.astype(float), win)
    m2 = uniform_filter((a*a).astype(float), win)
    return np.sqrt(np.clip(m2 - m*m, 0, None))

def detect(a, land_pct=80, k=1.3, smooth_pct=45, min_frac=0.0015):
    """Texture-aware adaptive-threshold dark-zone detector.
    Returns candidate mask + (mu, sigma, T) of the smooth-surface population."""
    sm = gaussian_filter(a, 1.5)
    tex = texture(sm, 11)
    smooth = tex < np.percentile(tex, smooth_pct)
    bright = sm > np.percentile(sm, land_pct)
    flat = smooth & ~bright
    flat = binary_closing(binary_opening(flat, iterations=2), iterations=3)
    fv = sm[flat]
    if fv.size == 0:
        return np.zeros_like(flat, bool), 0, 0, 0
    mu, sigma = fv.mean(), fv.std()
    T = max(mu - k*sigma, np.percentile(fv, 8))
    cand = flat & (sm < T)
    cand = binary_opening(cand, iterations=2)
    cand = binary_closing(cand, iterations=3)
    lbl, n = ndi.label(cand)
    sizes = ndi.sum(np.ones_like(lbl), lbl, range(1, n+1))
    keep = np.zeros_like(cand)
    for i, s in enumerate(sizes, 1):
        if s > a.size*min_frac:
            keep |= (lbl == i)
    return keep, mu, sigma, T

def style_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(GRID); s.set_linewidth(0.8)

def panel_label(ax, txt, x=0.012, y=0.965):
    ax.text(x, y, txt, transform=ax.transAxes, fontsize=12, fontweight='bold',
            color='black', va='top', ha='left',
            bbox=dict(boxstyle='square,pad=0.25', fc='white', ec=GRID, lw=0.6, alpha=0.92))

def arrow(ax, W, H, fx, fy, tx, ty, txt, col, fs=8.5):
    """Annotation: white label box w/ colored border at (tx,ty), arrow to (fx,fy)."""
    ax.add_patch(FancyArrowPatch((tx*W, ty*H), (fx*W, fy*H),
        arrowstyle='-|>', mutation_scale=12, color=col, lw=1.5,
        shrinkA=0, shrinkB=2))
    ax.text(tx*W, ty*H, txt, color='black', fontsize=fs, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=col, lw=1.3, alpha=0.95))

def stat_box(ax, W, H, txt):
    ax.text(0.015*W, 0.985*H, txt, color='black', fontsize=8, va='bottom', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=GRID, lw=0.6, alpha=0.9))

def overlay(ax, mask, H, W, rgb, alpha=0.40):
    ov = np.zeros((H, W, 4))
    ov[...,0]=rgb[0]; ov[...,1]=rgb[1]; ov[...,2]=rgb[2]; ov[...,3]=mask*alpha
    ax.imshow(ov, aspect='equal')
