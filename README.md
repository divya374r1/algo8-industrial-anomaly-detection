# Industrial Anomaly Detection for Cyclone Preheater Process

## 1. Project Overview

This project develops an industrial anomaly detection and decision-support system for identifying abnormal operating periods in a cyclone preheater process.

The system analyzes multivariate process sensor data, detects statistically unusual operating conditions, identifies persistent abnormal periods, characterizes the affected sensors, validates the detected events using PCA-based reconstruction error, and prioritizes events for operational investigation.

The project also includes a Streamlit-based dashboard for historical monitoring and anomaly investigation.

---

## 2. Problem Statement

Industrial process data contains multiple interacting sensor variables that can change due to different operating conditions.

Simple threshold-based monitoring may generate false alarms because a value that appears unusual in isolation may be normal under a particular operating regime.

The objective of this project is to:

- Detect multivariate abnormal operating conditions.
- Distinguish persistent abnormal behavior from short-lived spikes.
- Identify which sensors contribute most to each abnormal period.
- Classify abnormal events based on their multivariate impact.
- Prioritize events for operational investigation.
- Present the results through an interactive monitoring dashboard.

---

## 3. Dataset

The dataset contains approximately 377,719 records collected at approximately five-minute intervals over multiple years.

### Features

- `time`
- `Cyclone_Inlet_Gas_Temp`
- `Cyclone_Material_Temp`
- `Cyclone_Outlet_Gas_draft`
- `Cyclone_cone_draft`
- `Cyclone_Gas_Outlet_Temp`
- `Cyclone_Inlet_Draft`

The dataset contains both sensor measurements and connectivity-related entries such as `Not Connect`.

---

## 4. Data Quality and Preprocessing

Several data-quality challenges were identified before modeling.

### Timestamp Quality

The timestamp column contained multiple date formats. A format-aware parsing approach was used to correctly interpret both timestamp patterns.

### Sensor Connectivity

`Not Connect` entries were converted to missing numerical values during preprocessing.

Time-contiguous connectivity episodes were analyzed rather than treating all missing records as one continuous period.

### Missing Sensor Values

Records with incomplete sensor measurements were excluded from the six-sensor multivariate modeling matrix instead of applying blind imputation.

### Operating Regimes

A low-load operating regime was identified using zero cyclone material temperature observations.

This regime showed coordinated changes across multiple process variables and was therefore treated separately from the active operating regime.

---

## 5. Methodology

The analytical pipeline consists of the following stages:

```text
Raw Industrial Data
        ↓
Data Quality Analysis
        ↓
Timestamp Parsing
        ↓
Missing / Connectivity Handling
        ↓
Operating Regime Analysis
        ↓
Multivariate Feature Analysis
        ↓
Isolation Forest
        ↓
Anomaly Threshold Selection
        ↓
15-Minute Persistence Filtering
        ↓
Abnormal Event Characterization
        ↓
PCA-Based Validation
        ↓
Investigation Priority Scoring
        ↓
Streamlit Monitoring Dashboard