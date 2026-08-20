# Q-Shield: An Adaptive Multi-Agent Cyber-Risk Detection and Post-Quantum Security Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](LICENSE)
[![Framework: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Frontend: Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black.svg)](https://nextjs.org/)
[![PQC: NIST FIPS 203/204](https://img.shields.io/badge/PQC-ML--KEM%20%7C%20ML--DSA-blueviolet.svg)](https://csrc.nist.gov/Projects/post-quantum-cryptography)
[![Simulation: BB84 QKD](https://img.shields.io/badge/Quantum-BB84%20QKD%20%7C%20QRNG-success.svg)](https://en.wikipedia.org/wiki/BB84)

> **Computer Science & Engineering Final Year Major Project**  
> **Academic Cybersecurity Research & Safe Simulation Platform**

---

## 1. Executive Summary & Problem Statement

Modern distributed multi-agent systems and AI platforms rely heavily on autonomous software agents communicating across network boundaries. These distributed interactions introduce critical vulnerabilities including **man-in-the-middle (MITM) tampering, replay attacks, burst floods, rogue/unauthorized agents, and cryptographic credential compromises**. 

Conventional security systems rely on monolithic detectors and static threshold rules, which frequently produce high false-positive rates, blind spots, and brittle responses. Furthermore, classical cryptographic primitives (such as RSA and ECC) face existential threats from future quantum computers running Shor's algorithm.

**Q-Shield** introduces an intelligent, decentralized cybersecurity architecture where **specialized AI agents independently analyze distinct threat dimensions**, aggregate multi-source evidence, compute a dynamic hybrid risk score (combining machine learning and rule-based weights), and automatically orchestrate **adaptive post-quantum cryptographic (PQC) and quantum simulation defenses (QRNG, BB84 QKD)**.

---

## 2. Core Architectural Flow

```
+-----------------------------------------------------------------------------------+
|                            SYNTHETIC SECURITY EVENT                               |
|       (Heartbeat Telemetry, Message Exchange, File Transfer, Command Invocation)  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+--------------------+--------------------+--------------------+
|                    |                    |                    |
v                    v                    v                    v
[ Agent 1 ]          [ Agent 2 ]          [ Agent 3 ]          [ Agent 4 ]
Behavioral Agent     File Integrity Agent Trust / Verify Agent Risk Agent
(Rate & Bursts)      (SHA-256 Hashes)     (Zero-Trust Registry)(Evidence Aggregator)
|                    |                    |                    |
+--------------------+--------------------+--------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                              CENTRAL RISK ENGINE                                  |
|         Hybrid Risk = 0.60 * ML Probability + 0.40 * Rule-Based Evidence          |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        DYNAMIC RISK SCORE & CLASSIFICATION                        |
|       [ LOW: 0-30 ]            [ MEDIUM: 31-70 ]           [ HIGH: 71-100 ]       |
+-----------------------------------------------------------------------------------+
              |                           |                           |
              v                           v                           v
     +-----------------+         +-----------------+         +-----------------+
     | PQC Protection  |         | PQC + QRNG Sim  |         | PQC + QRNG + QKD|
     | (ML-KEM/ML-DSA) |         | (Quantum Nonces)|         | (Full Quarantine|
     |                 |         |                 |         | & Out-of-band)  |
     +-----------------+         +-----------------+         +-----------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            AGENT 5: FINAL DECISION AGENT                          |
|         Explainable Rationale + SHAP Feature Attribution + Security Policy        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                         SOC DASHBOARD & INCIDENT DOSSIER                          |
+-----------------------------------------------------------------------------------+
```

---

## 3. Specialized Multi-Agent Architecture

| Agent Name | Specialization & Focus | Detection Signals & Math |
| :--- | :--- | :--- |
| **Agent 1: Behavioral Agent** | Anomaly & Rate Analysis | Detects rate surges ($\ge 2.5\times$ baseline), burst floods (50 msgs/min), repeated payloads, and interval jitter. |
| **Agent 2: File Integrity Agent** | Cryptographic Hashing | Computes SHA-256 checksums: $\text{SHA256}(\text{pristine}) \neq \text{SHA256}(\text{current})$ indicates file/payload corruption. |
| **Agent 3: Risk Agent** | Evidence Aggregation | Normalizes and synthesizes cross-agent telemetry into unified JSON evidence without single-agent bias. |
| **Agent 4: Trust / Verification Agent** | Identity & Zero-Trust Registry | Validates agent authorization against trusted registries, tracks trust degradation, and flags unauthorized rogue agents. |
| **Agent 5: Final Decision Agent** | Adaptive Control Orchestration | Synthesizes composite risk scores into human-explainable rationale and commands adaptive PQC/quantum defense policies. |

---

## 4. Transparent Risk Scoring Engine & Adaptive Controls

### Modular Scoring Weights:
* **Unexpected / abnormal communication frequency**: `+50`
* **Authentication anomaly / invalid credentials**: `+20`
* **Message integrity violation / HMAC mismatch**: `+20`
* **Suspicious communication pattern / proxy hop**: `+10`
* **File integrity violation / SHA-256 mismatch**: `+30`
* **Unauthorized rogue agent ID**: `+30`
* **Replay attack detection / stale nonce**: `+30`
* **MITM simulation interception**: `+40`

$$\text{Raw Score} = \sum \text{Weights}, \quad \text{Normalized Rule Score} = \min(\text{Raw Score}, 100)$$

$$\text{Final Composite Risk} = 0.60 \times (\text{ML Anomaly Prob} \times 100) + 0.40 \times \text{Normalized Rule Score}$$

### Proportional Security Policy Matrix:
* **LOW RISK (0–30)**: Standard Post-Quantum Cryptography (ML-KEM-768 key encapsulation and ML-DSA-65 digital signatures) active.
* **MEDIUM RISK (31–70)**: PQC + **Quantum Random Number Generator (QRNG) simulation** activated. Nonces and session keys are refreshed with simulated quantum entropy to defeat replay predictability.
* **HIGH RISK (71–100)**: Full Defense Spectrum activated: PQC + QRNG + **BB84 Quantum Key Distribution (QKD) simulation** + Enhanced Zero-Trust Re-authentication + Agent Channel Quarantining.

---

## 5. Post-Quantum Cryptography & Quantum Simulators

1. **Post-Quantum Cryptography (PQC)**:
   - **NIST FIPS 203 (ML-KEM-768)**: Lattice-based Key Encapsulation Mechanism providing NIST Security Level 3 protection.
   - **NIST FIPS 204 (ML-DSA-65)**: Module-Lattice Digital Signature Algorithm providing quantum-resistant integrity verification.
2. **Quantum Random Number Generator (QRNG) Simulator**:
   - Simulates single-qubit and multi-qubit registers undergoing Hadamard superposition:
     $$|0\rangle \xrightarrow{H} \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$
   - Applies Born-rule measurement projection ($P=0.5$) with Shannon entropy calculation ($H \approx 1.0$).
3. **BB84 Quantum Key Distribution (QKD) Simulator**:
   - Educational simulation of photon polarization in Rectilinear ($+$) and Diagonal ($\times$) bases.
   - Public basis reconciliation and sifting.
   - Quantum Bit Error Rate (QBER) calculation: Without eavesdropper ($\text{QBER} = 0\%$), With Eve interceptor ($\text{QBER} \approx 25\% > 11\%$ threshold $\implies$ channel compromised alert).

---

## 6. Machine Learning & Explainable AI (SHAP)

* **Model**: Calibrated gradient-boosted logistic classifier trained on 1,500 synthetic multi-agent cybersecurity telemetry vectors.
* **Features (11)**: `message_frequency`, `frequency_ratio`, `auth_failure`, `unauthorized_agent`, `integrity_failure`, `replay_detected`, `mitm_indicator`, `trust_score`, `hash_mismatch`, `interval_jitter`, `payload_tampering`.
* **Explainability**: Computes exact Shapley Additive Explanations ($\phi_i$) for every telemetry feature, presenting point contributions (+/- score impact) to ensure complete auditability.

---

## 7. Project Structure

```
q-shield/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI server & lifespan startup hooks
│   │   ├── config.py                # Environment configurations & weights
│   │   ├── database/
│   │   │   ├── database.py          # SQLite/PostgreSQL persistence & connection pooling
│   │   │   └── schemas.py           # Pydantic data contracts & DTOs
│   │   ├── security/
│   │   │   └── auth.py              # JWT authentication & PBKDF2-SHA256 password hashing
│   │   ├── quantum/
│   │   │   ├── qrng.py              # Hadamard-superposition QRNG simulator
│   │   │   ├── qkd.py               # BB84 QKD protocol simulator (with Eve interceptor)
│   │   │   └── pqc.py               # NIST FIPS 203/204 ML-KEM & ML-DSA PQC services
│   │   ├── agents/
│   │   │   ├── base_agent.py        # Abstract base agent class
│   │   │   ├── behavioral_agent.py  # Agent 1: Rate & frequency analysis
│   │   │   ├── file_integrity_agent.py # Agent 2: SHA-256 checksum verification
│   │   │   ├── trust_agent.py       # Agent 4: Identity & authorization registry
│   │   │   ├── risk_agent.py        # Agent 3: Evidence aggregator
│   │   │   └── decision_agent.py    # Agent 5: Policy decision orchestrator
│   │   ├── risk/
│   │   │   ├── scoring.py           # Modular additive rule scoring engine
│   │   │   ├── policies.py          # Adaptive security policy selector
│   │   │   └── risk_engine.py       # Central hybrid risk engine
│   │   ├── ml/
│   │   │   ├── dataset.py           # Synthetic cybersecurity training dataset
│   │   │   ├── model.py             # Trained ML anomaly predictor
│   │   │   ├── explainability.py    # SHAP value attribution calculator
│   │   │   └── predictor.py         # End-to-end ML inference service
│   │   ├── simulator/
│   │   │   ├── normal.py            # Normal traffic generator
│   │   │   ├── mitm.py              # MITM attack scenario generator
│   │   │   ├── replay.py            # Replay attack scenario generator
│   │   │   ├── tampering.py         # File tampering scenario generator
│   │   │   ├── unauthorized_agent.py# Unauthorized rogue agent generator
│   │   │   └── repeated_message.py  # Traffic burst flood generator
│   │   └── api/
│   │       ├── auth.py              # Authentication endpoints
│   │       ├── dashboard.py         # SOC summary & charts endpoints
│   │       ├── agents.py            # Agents registry & metrics endpoints
│   │       ├── incidents.py         # Incident ledger & dossier endpoints
│   │       ├── simulator.py         # Simulation trigger endpoints
│   │       ├── quantum.py           # Quantum lab & PQC endpoints
│   │       └── analysis.py          # Custom event analysis endpoints
│   ├── tests/
│   │   ├── test_agents.py           # Multi-agent unit tests
│   │   ├── test_quantum.py          # QRNG & BB84 QKD tests
│   │   ├── test_pqc.py              # ML-KEM & ML-DSA tests
│   │   └── test_risk_engine.py      # Risk scoring & classification tests
│   ├── requirements.txt
│   └── run_server.py
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx           # Dark theme layout with CyberBackground
│   │   │   ├── page.tsx             # Project landing page
│   │   │   ├── dashboard/page.tsx   # Live SOC Operations Dashboard
│   │   │   ├── simulator/page.tsx   # Incident Simulator with 6 scenarios
│   │   │   ├── agents/page.tsx      # Agent Monitoring & Telemetry
│   │   │   ├── quantum/page.tsx     # Quantum Security & PQC Lab
│   │   │   ├── incidents/page.tsx   # Incident Audit Ledger with search/filter
│   │   │   ├── comparison/page.tsx  # Traditional vs Q-Shield benchmark matrix
│   │   │   └── report/page.tsx      # Printable/exportable dossier generator
│   │   ├── components/
│   │   │   ├── CyberBackground.tsx  # Interactive 3D particle Canvas visualizer
│   │   │   ├── RiskGauge.tsx        # Dynamic circular glowing risk gauge
│   │   │   ├── AgentCard.tsx        # Agent status & metrics card
│   │   │   ├── PipelineVisualizer.tsx # 5-Stage multi-agent pipeline visualizer
│   │   │   ├── QRNGVisualizer.tsx   # Interactive Hadamard quantum circuit
│   │   │   ├── QKDVisualizer.tsx    # Interactive BB84 photon polarization visualizer
│   │   │   ├── PQCInspector.tsx     # Interactive ML-KEM & ML-DSA testbench
│   │   │   ├── EvidencePanel.tsx    # Risk point contribution panel
│   │   │   ├── SecurityPolicyBadge.tsx # Adaptive control status badge
│   │   │   └── IncidentReportModal.tsx # Exportable incident report modal
│   │   ├── lib/
│   │   │   ├── api.ts               # Type-safe API client
│   │   │   └── utils.ts             # Styling helpers & color utilities
│   │   └── types/
│   │       └── security.ts          # TypeScript interfaces
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
└── start.sh
```

---

## 8. Installation & Execution Guide

### Prerequisites
* **Python**: 3.9+ (Python 3.11 recommended)
* **Node.js**: 18.0+ & npm 9.0+
* **Docker & Docker Compose** (Optional, for containerized deployment)

### Method A: Quick Launch with Single Command
```bash
# Clone or extract project repository
cd q-shield

# Run automated startup script
chmod +x start.sh
./start.sh
```

### Method B: Manual Step-by-Step Setup

#### Step 1: Start Backend
```bash
cd backend

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run unit tests to verify system integrity
python3 -m unittest discover tests

# Launch FastAPI backend
python3 run_server.py
```
* Backend will be running at: `http://localhost:8000`
* Interactive OpenAPI Documentation: `http://localhost:8000/docs`

#### Step 2: Start Frontend
```bash
# In a new terminal window
cd frontend

# Install Node dependencies
npm install

# Start Next.js development server
npm run dev
```
* Frontend will be accessible at: `http://localhost:3000`

---

## 9. Docker Deployment

To launch the complete multi-container system with Docker Compose:

```bash
docker-compose up --build
```
* Access SOC Dashboard: `http://localhost:3000`
* Access Backend API: `http://localhost:8000/docs`

---

## 10. Demonstration & Viva Walkthrough

1. **Step 1 (SOC Dashboard)**: Open `http://localhost:3000/dashboard`. Verify all 5 specialized agents are active and the composite risk gauge displays the system state.
2. **Step 2 (Normal Baseline)**: Open `http://localhost:3000/simulator`. Click `[Normal Traffic]`. Observe Risk Score < 30 (LOW) and standard PQC protection.
3. **Step 3 (Replay Attack)**: Click `[Replay Attack]`. Observe stale timestamp detection, risk escalating to MEDIUM (31-70), and automatic activation of the QRNG simulator.
4. **Step 4 (File Tampering)**: Click `[File Tampering]`. Observe SHA-256 checksum mismatch, risk escalating to HIGH (71-100), and QKD simulation activation.
5. **Step 5 (MITM Attack)**: Click `[MITM Attack Simulation]`. Observe multi-agent detection (auth anomaly + integrity violation + proxy hop), risk reaching ~99/100 (HIGH), and zero-trust channel quarantining.
6. **Step 6 (Quantum Lab)**: Open `http://localhost:3000/quantum`. Execute QRNG Hadamard measurement (entropy $\approx 1.0$). Run BB84 QKD simulation without Eve ($\text{QBER} = 0\%$, Secure) and with Eve ($\text{QBER} \approx 30\%$, Compromised Alert).
7. **Step 7 (Dossier Export)**: Open `http://localhost:3000/report`. Generate and download an immutable security incident audit report.

---

## 11. Academic Disclaimer & Limitations

* **Safe Simulation**: This platform is an educational research simulator. All attack scenarios utilize synthetic message events within isolated data structures. It does not perform actual network exploitation, packet sniffing, or external attacks.
* **Quantum Simulation**: The QRNG and BB84 QKD components are state-vector quantum simulations for educational demonstration. They do not connect to physical superconducting or photonic quantum hardware.
* **PQC Implementation**: Uses standardized mathematical abstractions of NIST FIPS 203 (ML-KEM-768) and FIPS 204 (ML-DSA-65) lattice cryptography.

---

## 12. Authors & Acknowledgments

* **Project Title**: Q-Shield: An Adaptive Multi-Agent Cyber-Risk Detection and Post-Quantum Security Framework
* **Academic Year**: 2025–2026
* **Domain**: Artificial Intelligence / Machine Learning, Multi-Agent Systems, Cybersecurity, Post-Quantum Cryptography
