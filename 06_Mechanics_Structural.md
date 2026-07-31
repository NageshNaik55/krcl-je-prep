# 06. Mechanics & Structural Engineering
# ಯಾಂತ್ರಿಕತೆ ಮತ್ತು ರಚನಾ ಎಂಜಿನಿಯರಿಂಗ್

---

# A. Strength of Materials | ವಸ್ತುಬಲಶಾಸ್ತ್ರ

## 1. Stress & Strain | ಒತ್ತಡ ಮತ್ತು ವಿರೂಪ
| Term | Formula | ಕನ್ನಡ |
|------|---------|-------|
| Stress (σ) | Force / Area = P/A | ಒತ್ತಡ |
| Strain (ε) | Change in length / Original = δL/L | ವಿರೂಪ |
| Young’s Modulus (E) | Stress / Strain = σ/ε | ಯಂಗ್ ಮಾಡ್ಯುಲಸ್ |
| Shear stress (τ) | Shear force / Area | ಕತ್ತರಿಸುವ ಒತ್ತಡ |
| Poisson’s ratio (μ) | Lateral strain / Longitudinal strain | ಪಾಯ್ಸನ್ ಅನುಪಾತ |

**Elastic constants:** E, G (shear modulus), K (bulk), μ  
ಸಂಬಂಧ: E = 2G(1+μ) = 3K(1−2μ)

**Hooke’s Law:** Stress ∝ Strain (within elastic limit)  
ಹೂಕ್ ನಿಯಮ: ಸ್ಥಿತಿಸ್ಥಾಪಕ ಮಿತಿಯಲ್ಲಿ ಒತ್ತಡ ∝ ವಿರೂಪ

---

## 2. SFD & BMD | ಕತ್ತರಿಸುವ ಬಲ ಮತ್ತು ಬಾಗುವ ಘಾತ ಚಿತ್ರಗಳು
- **Shear Force (SF):** Algebraic sum of vertical forces on one side.  
  ಕತ್ತರಿಸುವ ಬಲ
- **Bending Moment (BM):** Moment of forces about section.  
  ಬಾಗುವ ಘಾತ

**Sign tip (common convention):**
- Sagging BM positive (simply supported midspan).  
  ಕೆಳಗೆ ಬಾಗುವುದು ಧನಾತ್ಮಕ (ಸಾಮಾನ್ಯ)
- Left-up / right-down shear often positive.

**Must remember shapes:**
| Loading | SF shape | BM shape |
|---------|----------|----------|
| Point load | Rectangle jump | Triangle |
| UDL | Triangle / Trapezoid | Parabola |
| UVL | Parabola | Cubic |

**Relation:** dM/dx = SF ; dSF/dx = −w  
Max BM where SF = 0.

**Simply supported, span L, load W at mid:**
- Max BM = WL/4  
- Max SF = W/2

**UDL w over span L:**
- Max BM = wL²/8  
- Max SF = wL/2

---

# B. RCC Design | ಆರ್‌ಸಿಸಿ ವಿನ್ಯಾಸ

## 1. Methods | ವಿಧಾನಗಳು
| Method | Idea | ಕನ್ನಡ |
|--------|------|-------|
| Working Stress Method (WSM) | Permissible stress based | ಕಾರ್ಯ ಒತ್ತಡ ವಿಧಾನ |
| Limit State Method (LSM) | Safety against collapse & serviceability (preferred now) | ಮಿತಿ ಸ್ಥಿತಿ ವಿಧಾನ |

**Partial safety factors (LSM common):**
- Concrete: 1.5  
- Steel: 1.15  
- Dead load: 1.5 ; Live load: 1.5 (basic combinations vary)

---

## 2. Beams | ಕಿರಣಗಳು
- Under-reinforced → steel fails first (ductile) — preferred.  
  ಕಡಿಮೆ ಉಕ್ಕು = ಇಚ್ಛಿತ (ಡಕ್ಟೈಲ್)
- Over-reinforced → concrete fails first (brittle) — avoid.  
  ಹೆಚ್ಚು ಉಕ್ಕು = ತಪ್ಪಿಸಿ
- Balanced → both reach limit together.

**Main steel** resists tension; **stirrups** resist shear.  
ಮುಖ್ಯ ಉಕ್ಕು = ಎಳೆತ; ಸ್ಟಿರಪ್ = ಕತ್ತರಿಸುವ ಬಲ.

---

## 3. Slabs | ಫಲಕಗಳು
- One-way slab: Ly/Lx > 2 → main steel shorter span.  
  ಏಕಮಾರ್ಗ ಫಲಕ
- Two-way slab: Ly/Lx ≤ 2 → steel in both directions.  
  ದ್ವಿಮಾರ್ಗ ಫಲಕ
- Thickness decided by span/depth ratios & deflection control.

---

## 4. Columns | ಕಂಬಗಳು
- Short column vs Long (slender) column.  
  ಕಿರು ಕಂಬ / ಉದ್ದ ಕಂಬ
- Axially loaded / Eccentrically loaded.  
  ಅಕ್ಷೀಯ / ವಿಕೇಂದ್ರೀಯ ಭಾರ
- Lateral ties / helical reinforcement prevent buckling of bars.  
  ಟೈಗಳು ಬಾರ್‌ಗಳ ಬಾಗುವಿಕೆಯನ್ನು ತಡೆಯುತ್ತವೆ.

**IS tip:** Min eccentricity, min longitudinal steel ~ 0.8%, max ~ 4% (as per code practice).

---

## 5. Shear Reinforcement | ಕತ್ತರಿಸುವ ಬಲ ಬಲವರ್ಧನೆ
- Vertical stirrups most common.  
  ಲಂಬ ಸ್ಟಿರಪ್‌ಗಳು
- Bent-up bars also used.  
  ಬಾಗಿಸಿದ ಬಾರ್‌ಗಳು
- Provide where shear force is high (near supports).  
  ಆಧಾರಗಳ ಹತ್ತಿರ ಹೆಚ್ಚು.

---

# C. Steel Design | ಉಕ್ಕು ವಿನ್ಯಾಸ

## 1. Steel Sections | ಉಕ್ಕಿನ ವಿಭಾಗಗಳು
- I-section, Channel (C), Angle (L), T, Plate, Tube, HSS.  
  ಐ, ಚಾನಲ್, ಕೋನ, ಟಿ, ಪ್ಲೇಟ್
- Rolled / Built-up sections.  
  ರೋಲ್ಡ್ / ನಿರ್ಮಿತ ವಿಭಾಗಗಳು

---

## 2. Riveted & Welded Joints | ರಿವೆಟ್ ಮತ್ತು ವೆಲ್ಡ್ ಜಂಟ್‌ಗಳು
**Riveted (older):**
- Strength governed by shearing / bearing / tearing of plate.  
  ಕತ್ತರಿಸುವ / ಒತ್ತುವ / ಹರಿಯುವ ಬಲ

**Welded (common now):**
- Fillet weld / Butt weld  
  ಫಿಲೆಟ್ / ಬಟ್ ವೆಲ್ಡ್
- Throat thickness for fillet = 0.7 × size (approx).  
  ಗಂಟಲು ದಪ್ಪ ≈ 0.7 × ಗಾತ್ರ

---

## 3. Tension Members | ಎಳೆತ ಸದಸ್ಯರು
- Carry tensile force (e.g., bottom chord of truss).  
  ಎಳೆತ ಬಲ ಹೊರುವ ಸದಸ್ಯ
- Net effective area important (deduct bolt holes).  
  ನಿವ್ವಳ ಪರಿಣಾಮಕಾರಿ ವಿಸ್ತೀರ್ಣ ಮುಖ್ಯ.

---

## 4. Compression Members | ಸಂಕೋಚನ ಸದಸ್ಯರು
- Columns, struts — buckling decides capacity.  
  ಕಂಬ / ಸ್ಟ್ರಟ್ — ಬಾಗುವಿಕೆ ನಿರ್ಧಾರಕ
- Slenderness ratio = Le / r  
  ಪತಳತೆ ಅನುಪಾತ = ಪರಿಣಾಮಕಾರಿ ಉದ್ದ / ತ್ರಿಜ್ಯ ಆಫ್ ಗೈರೇಷನ್
- Higher slenderness → lower capacity.  
  ಹೆಚ್ಚು ಪತಳತೆ = ಕಡಿಮೆ ಸಾಮರ್ಥ್ಯ

---

## Formula Snapshot | ಸೂತ್ರ ಸ್ನ್ಯಾಪ್‌ಶಾಟ್
1. σ = P/A ; ε = δL/L ; E = σ/ε  
2. Simply supported mid point load: M = WL/4  
3. UDL on SS beam: M = wL²/8  
4. Prefer under-reinforced RCC beams  
5. Fillet weld throat ≈ 0.7t  

**ಅಭ್ಯಾಸ ಸಲಹೆ:** SFD/BMD ಚಿತ್ರಗಳನ್ನು ಪ್ರತಿದಿನ 2–3 ಬರೆಯಿರಿ. RCC ನಲ್ಲಿ under/over reinforced ಪರಿಕಲ್ಪನೆ ಖಚಿತವಾಗಿ ನೆನಪಿಡಿ.
