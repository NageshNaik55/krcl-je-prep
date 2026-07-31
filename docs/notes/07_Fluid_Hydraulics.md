# 07. Fluid Mechanics & Hydraulics
# ದ್ರವ ಯಾಂತ್ರಿಕತೆ ಮತ್ತು ಜಲಶಾಸ್ತ್ರ

---

## 1. Fluid Properties | ದ್ರವದ ಗುಣಗಳು

| Property | Meaning | ಕನ್ನಡ |
|----------|---------|-------|
| Density (ρ) | Mass / Volume | ಸಾಂದ್ರತೆ |
| Specific weight (γ) | Weight / Volume = ρg | ನಿರ್ದಿಷ್ಟ ತೂಕ |
| Specific gravity (S) | Density of fluid / Density of water | ನಿರ್ದಿಷ್ಟ ಗುರುತ್ವ |
| Viscosity (μ) | Resistance to flow (internal friction) | ಸ್ನಿಗ್ಧತೆ |
| Kinematic viscosity (ν) | μ/ρ | ಚಲನ ಸ್ನಿಗ್ಧತೆ |
| Surface tension (σ) | Force along surface per unit length | ಪೊರೆ ಒತ್ತಡ |
| Capillarity | Rise/fall in narrow tube | ಕ್ಯಾಪಿಲರಿ |

**Water (standard):** ρ ≈ 1000 kg/m³ ; S = 1 ; γ ≈ 9810 N/m³

---

## 2. Fluid Pressure | ದ್ರವ ಒತ್ತಡ
- Pressure P = ρ g h = γ h  
  ಒತ್ತಡ = ಸಾಂದ್ರತೆ × g × ಆಳ
- Pressure increases with depth.  
  ಆಳ ಹೆಚ್ಚಾದಂತೆ ಒತ್ತಡ ಹೆಚ್ಚು.
- Absolute = Atmospheric + Gauge  
  ಪರಿಪೂರ್ಣ = ವಾತಾವರಣ + ಗೇಜ್
- Vacuum pressure = Atmospheric − Absolute

**Measurement devices:** Piezometer, Manometer, Bourdon gauge, Pressure transducer.  
ಪೈಝೋಮೀಟರ್, ಮ್ಯಾನೋಮೀಟರ್, ಬೌರ್ಡನ್ ಗೇಜ್.

---

## 3. Continuity Equation | ನಿರಂತರತೆ ಸಮೀಕರಣ
For incompressible fluid:  
**A1 V1 = A2 V2 = Q (discharge)**

ವಿಸ್ತೀರ್ಣ × ವೇಗ = ಸ್ರಾವ (ನಿರಂತರ)

Meaning: When area decreases, velocity increases.  
ವಿಸ್ತೀರ್ಣ ಕಡಿಮೆಯಾದರೆ ವೇಗ ಹೆಚ್ಚು.

---

## 4. Bernoulli’s Theorem | ಬರ್ನೂಲಿ ಪ್ರಮೇಯ
Along a streamline (ideal fluid):  
**P/γ + V²/2g + z = constant**

| Term | Name | ಕನ್ನಡ |
|------|------|-------|
| P/γ | Pressure head | ಒತ್ತಡ ಶಿರ |
| V²/2g | Velocity head | ವೇಗ ಶಿರ |
| z | Datum / elevation head | ಎತ್ತರ ಶಿರ |

**Practical:** Venturimeter, Orificemeter, Pitot tube use Bernoulli.  
ವೆಂಚುರಿ, ಒರಿಫಿಸ್, ಪಿಟಾಟ್ ಟ್ಯೂಬ್.

---

## 5. Flow Through Pipes | ಪೈಪ್‌ಗಳಲ್ಲಿ ಹರಿವು
**Darcy–Weisbach head loss:**  
hf = (f L V²) / (2 g D)

| Symbol | Meaning | ಅರ್ಥ |
|--------|---------|------|
| f | Friction factor | ಘರ್ಷಣ ಅಂಶ |
| L | Length | ಉದ್ದ |
| V | Velocity | ವೇಗ |
| D | Diameter | ವ್ಯಾಸ |

**Other losses:** Entry, Exit, Bend, Sudden enlargement/contraction.  
ಪ್ರವೇಶ, ನಿರ್ಗಮನ, ಬಾಗುವಿಕೆ, ಹಠಾತ್ ವಿಸ್ತರಣ/ಸಂಕೋಚನ.

**Laminar vs Turbulent:**
- Reynolds number Re = ρVD/μ  
- Re < 2000 → Laminar | ಪದರೀಯ  
- Re > 4000 → Turbulent | ಪ್ರಕ್ಷುಬ್ಧ

---

## 6. Open Channel Flow | ತೆರೆದ ಕಾಲುವೆ ಹರಿವು
- Flow with free surface (canals, rivers).  
  ಮುಕ್ತ ಮೇಲ್ಮೈಯ ಹರಿವು (ಕಾಲುವೆ, ನದಿ)
- Chezy: V = C √(m i)  
- Manning: V = (1/n) R^(2/3) S^(1/2)  
  n = roughness coefficient | ಒರಟುತನ ಗುಣಾಂಕ
- Most economical rectangular section: Depth = Width/2  
  ಅತ್ಯಂತ ಆರ್ಥಿಕ ಆಯತಾಕಾರ: ಆಳ = ಅಗಲ/2

---

## 7. Hydrology Basics | ಜಲವಿಜ್ಞಾನ ಮೂಲಗಳು

### Rainfall measurement | ಮಳೆ ಅಳತೆ
- Instrument: Rain gauge (Symon’s gauge common in India)  
  ಮಳೆಮಾಪಕ
- Intensity = rainfall / time  
  ತೀವ್ರತೆ = ಮಳೆ / ಕಾಲ

### Run-off | ಹರಿವು (ರನ್-ಆಫ್)
- Portion of rainfall that flows on surface.  
  ಮಳೆಯಲ್ಲಿ ಮೇಲ್ಮೈಯಲ್ಲಿ ಹರಿಯುವ ಭಾಗ.
- Depends on: slope, soil, vegetation, rainfall intensity.  
  ಇಳಿಜಾರು, ಮಣ್ಣು, ಸಸ್ಯವರ್ಗ, ಮಳೆ ತೀವ್ರತೆ.
- Run-off = Rainfall − Losses (infiltration, evaporation, interception)

### Crop Water Requirement | ಬೆಳೆ ನೀರಿನ ಅಗತ್ಯ
- Delta (Δ) = total water depth required by crop.  
  ಡೆಲ್ಟಾ = ಬೆಳೆಗೆ ಬೇಕಾದ ಒಟ್ಟು ನೀರಿನ ಆಳ
- Duty (D) = area irrigated by unit discharge.  
  ಡ್ಯೂಟಿ = ಘಟಕ ಸ್ರಾವದಿಂದ ನೀರಾವರಿ ವಿಸ್ತೀರ್ಣ
- Relation: **Δ = 8.64 B / D** (B = base period in days; units consistent)  
  (Common exam relation — remember with correct units as taught)

**Base period:** Time from first to last watering of crop.  
ಬೇಸ್ ಪೀರಿಯಡ್ = ಮೊದಲಿನಿಂದ ಕೊನೆಯ ನೀರಾವರಿ ಕಾಲ.

---

## 8. Basic Irrigation Structures | ಮೂಲ ನೀರಾವರಿ ರಚನೆಗಳು
| Structure | Function | ಕಾರ್ಯ |
|-----------|----------|-------|
| Weir / Barrage | Raise water level / divert | ನೀರಿನ ಮಟ್ಟ ಏರಿಸುವ / ತಿರುಗಿಸುವ |
| Canal | Convey irrigation water | ಕಾಲುವೆ |
| Head regulator | Control entry to canal | ಪ್ರವೇಶ ನಿಯಂತ್ರಣ |
| Cross drainage | Canal crosses drain/river | ಅಡ್ಡ ಜಲನಿರ್ಗಮನ |
| Escape | Remove surplus water | ಹೆಚ್ಚುವರಿ ನೀರು ತೆಗೆಯುವುದು |
| Outlet | Supply to field channel | ಹೊಲಕ್ಕೆ ನೀರು |

---

## Must Score Points | ಅನಿವಾರ್ಯ ಅಂಕಗಳು
1. P = ρgh  
2. A1V1 = A2V2  
3. Bernoulli: P/γ + V²/2g + z = const  
4. Re decides laminar/turbulent  
5. Rain gauge measures rainfall  

**ಅಭ್ಯಾಸ:** ಬರ್ನೂಲಿ ಮತ್ತು ನಿರಂತರತೆ ಸಮೀಕರಣದ ಸಂಖ್ಯಾತ್ಮಕ ಪ್ರಶ್ನೆಗಳು ಹೆಚ್ಚು ಬರುತ್ತವೆ.
