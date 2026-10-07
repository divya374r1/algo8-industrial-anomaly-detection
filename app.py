import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cyclone Preheater | Industrial Anomaly Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL LIGHT INDUSTRIAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f4f6f8;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #eef1f4;
        border-right: 1px solid #d9dee3;
    }

    /* Main title */
    .main-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #243447;
        margin-bottom: 0.25rem;
    }

    .subtitle {
        color: #66727f;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Section headings */
    .section-title {
        color: #263746;
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1.2rem;
        margin-bottom: 0.7rem;
    }

    /* KPI cards */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #dfe4e8;
        border-radius: 12px;
        padding: 18px 18px 15px 18px;
        min-height: 115px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    .kpi-label {
        color: #6b7785;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .kpi-value {
        color: #263746;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 8px;
    }

    .kpi-note {
        color: #7b8794;
        font-size: 0.75rem;
        margin-top: 4px;
    }

    /* Investigation box */
    .investigation-box {
        background-color: #ffffff;
        border: 1px solid #dfe4e8;
        border-left: 5px solid #526d82;
        border-radius: 10px;
        padding: 18px;
        margin-top: 10px;
    }

    /* Small status badges */
    .status-high {
        color: #a33a3a;
        font-weight: 700;
    }

    .status-medium {
        color: #946b20;
        font-weight: 700;
    }

    .status-low {
        color: #4f6f5b;
        font-weight: 700;
    }

    /* Footer */
    .footer {
        color: #7a858f;
        font-size: 0.78rem;
        text-align: center;
        padding-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    monitoring = pd.read_csv(
        "data/monitoring_data.csv",
        parse_dates=["time"]
    )

    events = pd.read_csv(
        "data/abnormal_periods_with_priority.csv",
        parse_dates=["start_time", "end_time"]
    )

    return monitoring, events


monitoring, events = load_data()


# ============================================================
# SENSOR LIST
# ============================================================

sensor_columns = [
    "Cyclone_Inlet_Gas_Temp",
    "Cyclone_Material_Temp",
    "Cyclone_Outlet_Gas_draft",
    "Cyclone_cone_draft",
    "Cyclone_Gas_Outlet_Temp",
    "Cyclone_Inlet_Draft"
]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🏭 Cyclone Preheater Industrial Anomaly Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Multivariate anomaly detection, temporal persistence, event explanation '
    'and investigation prioritization for industrial process monitoring.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🔎 Investigation Filters")

priority_options = sorted(
    events["priority_level"].dropna().unique().tolist()
)

event_type_options = sorted(
    events["event_type"].dropna().unique().tolist()
)

sensor_options = sorted(
    events["dominant_sensor"].dropna().unique().tolist()
)

priority_filter = st.sidebar.multiselect(
    "Priority Level",
    priority_options,
    default=priority_options
)

event_type_filter = st.sidebar.multiselect(
    "Event Type",
    event_type_options,
    default=event_type_options
)

sensor_filter = st.sidebar.multiselect(
    "Dominant Sensor",
    sensor_options,
    default=sensor_options
)

filtered_events = events[
    events["priority_level"].isin(priority_filter)
    & events["event_type"].isin(event_type_filter)
    & events["dominant_sensor"].isin(sensor_filter)
].copy()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_events = len(events)

system_wide_events = int(
    events["event_type"]
    .eq("System-wide multivariate deviation")
    .sum()
)

multisensor_events = int(
    (events["abnormal_sensor_count"] >= 2).sum()
)

persistent_records = int(
    monitoring["event_id"].notna().sum()
)

high_priority_events = int(
    events["priority_level"].eq("High").sum()
)

longest_event = float(
    events["duration_minutes"].max()
)


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

kpis = [
    ("Abnormal Events", f"{total_events}", "Final persistent events"),
    ("System-wide", f"{system_wide_events}", "Process-level events"),
    ("Multi-sensor", f"{multisensor_events}", "2+ sensors affected"),
    ("Persistent Records", f"{persistent_records:,}", "Records in events"),
    ("High Priority", f"{high_priority_events}", "Investigation queue"),
    ("Longest Event", f"{longest_event:.0f} min", "Maximum duration")
]

for col, (label, value, note) in zip(
    [kpi1, kpi2, kpi3, kpi4, kpi5, kpi6],
    kpis
):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# TABS
# ============================================================

tab_overview, tab_investigate, tab_replay = st.tabs(
    [
        "📊 Operations Overview",
        "🔬 Event Investigation",
        "⏱️ Historical Monitoring Replay"
    ]
)


# ============================================================
# TAB 1 — OPERATIONS OVERVIEW
# ============================================================

with tab_overview:

    st.markdown(
        '<div class="section-title">📈 Anomaly Score Timeline</div>',
        unsafe_allow_html=True
    )

    # Downsample normal observations for faster visualization
    # while preserving all anomalous observations.
    normal_points = monitoring[
        ~monitoring["anomaly_flag"]
    ].iloc[::20]

    anomaly_points = monitoring[
        monitoring["anomaly_flag"]
    ]

    timeline_display = pd.concat(
        [normal_points, anomaly_points]
    ).drop_duplicates(
        subset=["time"]
    ).sort_values("time")

    fig_timeline = px.line(
        timeline_display,
        x="time",
        y="anomaly_score",
        labels={
            "time": "Time",
            "anomaly_score": "Isolation Forest Anomaly Score"
        }
    )

    fig_timeline.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig_timeline,
        use_container_width=True
    )

    st.caption(
        "The timeline displays the anomaly score across the historical "
        "operating period. Higher scores indicate more unusual observations."
    )


    # --------------------------------------------------------
    # TWO ANALYSIS CHARTS
    # --------------------------------------------------------

    chart1, chart2 = st.columns(2)

    with chart1:

        event_type_counts = (
            filtered_events["event_type"]
            .value_counts()
            .reset_index()
        )

        event_type_counts.columns = [
            "event_type",
            "count"
        ]

        fig_event_type = px.bar(
            event_type_counts,
            x="event_type",
            y="count",
            title="Abnormal Event Classification",
            labels={
                "event_type": "Event Type",
                "count": "Events"
            }
        )

        fig_event_type.update_layout(
            height=430,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            xaxis_tickangle=-20
        )

        st.plotly_chart(
            fig_event_type,
            use_container_width=True
        )


    with chart2:

        sensor_counts = (
            filtered_events["dominant_sensor"]
            .value_counts()
            .sort_values()
            .reset_index()
        )

        sensor_counts.columns = [
            "sensor",
            "count"
        ]

        fig_sensor = px.bar(
            sensor_counts,
            x="count",
            y="sensor",
            orientation="h",
            title="Dominant Sensor Contribution",
            labels={
                "sensor": "Dominant Sensor",
                "count": "Events"
            }
        )

        fig_sensor.update_layout(
            height=430,
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff"
        )

        st.plotly_chart(
            fig_sensor,
            use_container_width=True
        )


    # --------------------------------------------------------
    # DURATION
    # --------------------------------------------------------

    fig_duration = px.histogram(
        filtered_events,
        x="duration_minutes",
        nbins=20,
        title="Abnormal Event Duration Distribution",
        labels={
            "duration_minutes": "Duration (minutes)",
            "count": "Events"
        }
    )

    fig_duration.update_layout(
        height=400,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )

    st.plotly_chart(
        fig_duration,
        use_container_width=True
    )


    # --------------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">💡 Industrial Insights</div>',
        unsafe_allow_html=True
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.info(
            "**78.95%** of abnormal events involve multiple abnormal "
            "sensors, indicating that many detected events are "
            "process-level rather than isolated sensor deviations."
        )

    with col_b:
        st.info(
            "**71.58%** of events have a temperature variable as the "
            "dominant sensor, highlighting temperature behavior as "
            "an important investigation area."
        )

    with col_c:
        st.info(
            "The longest detected event persisted for **535 minutes**, "
            "showing why temporal persistence is useful for prioritizing "
            "operational investigation."
        )


# ============================================================
# TAB 2 — EVENT INVESTIGATION
# ============================================================

with tab_investigate:

    st.markdown(
        '<div class="section-title">🚨 Investigation Priority Queue</div>',
        unsafe_allow_html=True
    )

    queue_columns = [
        "event_id",
        "priority_level",
        "priority_score",
        "start_time",
        "end_time",
        "duration_minutes",
        "event_type",
        "dominant_sensor",
        "dominant_direction",
        "abnormal_sensor_count",
        "pca_validated"
    ]

    queue_df = (
        filtered_events[queue_columns]
        .sort_values(
            "priority_score",
            ascending=False
        )
        .copy()
    )

    st.dataframe(
        queue_df,
        use_container_width=True,
        hide_index=True
    )


    st.markdown(
        '<div class="section-title">🔬 Event Investigation Report</div>',
        unsafe_allow_html=True
    )

    if len(filtered_events) > 0:

        selected_event = st.selectbox(
            "Select an abnormal event",
            filtered_events["event_id"].tolist()
        )

        selected = events[
            events["event_id"] == selected_event
        ].iloc[0]


        # ----------------------------------------------------
        # EVENT METRICS
        # ----------------------------------------------------

        e1, e2, e3, e4 = st.columns(4)

        with e1:
            st.metric(
                "Priority",
                str(selected["priority_level"])
            )

        with e2:
            st.metric(
                "Priority Score",
                f"{selected['priority_score']:.1f}"
            )

        with e3:
            st.metric(
                "Duration",
                f"{selected['duration_minutes']:.0f} min"
            )

        with e4:
            st.metric(
                "Abnormal Sensors",
                int(selected["abnormal_sensor_count"])
            )


        # ----------------------------------------------------
        # EVENT CHARACTERISTICS
        # ----------------------------------------------------

        left, right = st.columns(2)

        with left:

            st.markdown("### Event Characteristics")

            st.write(
                f"**Start:** {selected['start_time']}"
            )

            st.write(
                f"**End:** {selected['end_time']}"
            )

            st.write(
                f"**Event Type:** {selected['event_type']}"
            )

            st.write(
                f"**Dominant Sensor:** {selected['dominant_sensor']}"
            )

            st.write(
                f"**Direction:** {selected['dominant_direction']}"
            )


        with right:

            st.markdown("### Statistical Evidence")

            st.write(
                f"**Maximum Anomaly Score:** "
                f"{selected['max_score']:.3f}"
            )

            st.write(
                f"**Mean Anomaly Score:** "
                f"{selected['mean_score']:.3f}"
            )

            st.write(
                f"**Dominant Robust Z-score:** "
                f"{selected['dominant_robust_z']:.2f}"
            )

            st.write(
                f"**PCA Validation:** "
                f"{'Supported' if selected['pca_validated'] else 'Not supported'}"
            )


        # ----------------------------------------------------
        # SENSOR SNAPSHOT
        # ----------------------------------------------------

        st.markdown("### 📡 Sensor Snapshot During Event")

        event_rows = monitoring[
            monitoring["event_id"] == selected_event
        ]

        if len(event_rows) > 0:

            sensor_snapshot = pd.DataFrame({
                "Sensor": sensor_columns,
                "Event Median": [
                    event_rows[s].median()
                    for s in sensor_columns
                ],
                "Event Minimum": [
                    event_rows[s].min()
                    for s in sensor_columns
                ],
                "Event Maximum": [
                    event_rows[s].max()
                    for s in sensor_columns
                ]
            })

            st.dataframe(
                sensor_snapshot,
                use_container_width=True,
                hide_index=True
            )


        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        st.markdown("### 🧭 Recommended Investigation")

        if selected["event_type"] == "System-wide multivariate deviation":

            recommendation = (
                "Prioritize this event for process-level investigation. "
                "Multiple process variables deviated together. Review "
                "operating conditions, production context and maintenance "
                "records during the abnormal interval."
            )

        elif selected["event_type"] == "Multi-sensor deviation":

            recommendation = (
                "Investigate the coordinated behavior of the affected "
                "sensors. Compare the event interval with process logs "
                "and operating conditions to determine whether the "
                "deviation represents a meaningful process change."
            )

        else:

            recommendation = (
                "Review the dominant sensor and surrounding process "
                "variables. Check whether the deviation is associated "
                "with sensor quality, instrumentation behavior or a "
                "localized process condition."
            )

        st.info(recommendation)

        st.caption(
            "This system identifies statistically abnormal operating "
            "periods. It does not claim confirmed equipment failure or "
            "root cause because the dataset does not contain failure "
            "or root-cause labels."
        )

    else:

        st.warning(
            "No events match the selected filters."
        )


# ============================================================
# TAB 3 — HISTORICAL MONITORING REPLAY
# ============================================================

with tab_replay:

    st.markdown(
        '<div class="section-title">⏱️ Historical Sensor Replay</div>',
        unsafe_allow_html=True
    )

    st.write(
        "This prototype replays historical sensor observations to "
        "demonstrate how the monitoring system could operate when "
        "observations arrive sequentially from an industrial process."
    )

    # Reduce slider size to approximately one point per 15 minutes
    replay_indices = np.linspace(
        0,
        len(monitoring) - 1,
        min(2500, len(monitoring)),
        dtype=int
    )

    selected_index = st.slider(
        "Move through historical operating time",
        min_value=0,
        max_value=len(replay_indices) - 1,
        value=0
    )

    current_row = monitoring.iloc[
        replay_indices[selected_index]
    ]

    current_time = current_row["time"]

    st.markdown(
        f"### Current Process Snapshot — {current_time}"
    )


    # --------------------------------------------------------
    # CURRENT STATUS
    # --------------------------------------------------------

    if pd.notna(current_row["event_id"]):

        current_status = "⚠️ Persistent Abnormal Event"
        status_description = (
            f"Event {current_row['event_id']} is active."
        )

    elif current_row["anomaly_flag"]:

        current_status = "🟡 Point Anomaly"
        status_description = (
            "The observation exceeds the Isolation Forest threshold "
            "but is not part of a final persistent abnormal event."
        )

    else:

        current_status = "🟢 Normal Operating Observation"
        status_description = (
            "No anomaly threshold exceedance at this observation."
        )


    st.info(
        f"**Status: {current_status}**\n\n"
        f"{status_description}"
    )


    # --------------------------------------------------------
    # CURRENT SENSOR VALUES
    # --------------------------------------------------------

    sensor_values = pd.DataFrame({
        "Sensor": sensor_columns,
        "Current Value": [
            current_row[s]
            for s in sensor_columns
        ]
    })

    st.dataframe(
        sensor_values,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # CURRENT ANOMALY SCORE
    # --------------------------------------------------------

    replay_col1, replay_col2, replay_col3 = st.columns(3)

    with replay_col1:

        st.metric(
            "Anomaly Score",
            f"{current_row['anomaly_score']:.3f}"
        )

    with replay_col2:

        st.metric(
            "Persistent Event",
            "Yes" if pd.notna(current_row["event_id"]) else "No"
        )

    with replay_col3:

        st.metric(
            "Event ID",
            str(current_row["event_id"])
            if pd.notna(current_row["event_id"])
            else "—"
        )


    st.caption(
        "Prototype limitation: this replay uses historical sensor data. "
        "A production implementation would replace the historical file "
        "with a live SCADA/PLC/MES data stream."
    )


# ============================================================
# METHODOLOGY
# ============================================================

st.divider()

with st.expander("🧠 Detection Methodology"):

    st.markdown(
        """
        **Detection pipeline**

        1. Historical cyclone-preheater sensor data was cleaned and
           chronologically aligned.
        2. Low-load operating conditions were separated from active
           operation.
        3. Isolation Forest was applied to the multivariate process
           variables.
        4. The 99.5th-percentile anomaly score was selected as the
           detection threshold.
        5. A minimum 15-minute persistence requirement was applied
           to reduce isolated transient spikes.
        6. Persistent observations were consolidated into abnormal
           operating periods.
        7. Events were characterized using robust sensor deviation,
           event type and dominant-sensor analysis.
        8. PCA reconstruction error was used as an independent
           multivariate validation signal.
        9. An investigation-priority score combines severity,
           persistence, multivariate impact and PCA evidence.

        **Important:** The priority score is an investigation-support
        ranking. It is not a probability of equipment failure.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
    Cyclone Preheater Industrial Anomaly Intelligence Prototype
    <br>
    Isolation Forest • Temporal Persistence • Robust Event Profiling • PCA Validation
    </div>
    """,
    unsafe_allow_html=True
)