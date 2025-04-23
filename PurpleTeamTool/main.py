import streamlit as st
import pandas as pd
import purple
from red import red_team
from mediator import AIModel
from log_manager import log_attack, ATTACK_LOG_FILE, DETECTION_LOG_FILE
import time

ai = AIModel(api_key="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", model_name="mistralai/Mixtral-8x7B-Instruct-v0.1")

# Right after imports
st.markdown("""
    <style>
        .block-container {
            max-width: 95vw !important;
            padding-left: 20rem !important;
            padding-right: 20rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Title and Layout
st.title("Purple Team Security Tool")

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Red Team (Attack)"

tab_labels = ["Red Team (Attack)", "Purple Team Analysis", "Blue Team (Defense)"]
tabs = st.tabs(tab_labels)
red_tab, purple_tab, blue_tab = tabs

# Streamlit workaround: session state active tab
for idx, label in enumerate(tab_labels):
    if tabs[idx]:
        st.session_state.active_tab = label

with red_tab:
    st.header("Red Team (Attack)")

    if st.button("Basic SQL Injection"):
        st.text_area("Red Team Log", red_team.sqli_basic(), height=200)

    if st.button("Basic XSS"):
        st.text_area("Red Team Log", red_team.xss_basic(), height=200)

    if st.button("Command Injection"):
        st.text_area("Red Team Log", red_team.command_injection(), height=200)

    if st.button("Basic LFI"):
        st.text_area("Red Team Log", red_team.lfi_basic(), height=200)

    if st.button("False Positive - SQL Keyword"):
        st.text_area("Red Team Log", red_team.false_positive(), height=200)

with purple_tab:
    st.header("Purple Team Analysis")

    results = purple.run_purple_team_analysis(ATTACK_LOG_FILE, DETECTION_LOG_FILE)

    # Helper to flatten logs
    def flatten_entry(entry, category_label):
        flat = {
            "category": category_label,
            "timestamp": entry.get("timestamp", ""),
            "event_type": entry.get("event_type", ""),
            "target": entry.get("target", ""),
            "attacker_ip": entry.get("attacker_ip", ""),
            "source_ip": entry.get("source_ip", "")
        }

        # Flatten details if present
        details = entry.get("details", {})
        for key, value in details.items():
            flat[key] = value

        return flat

    # Prepare rows for all categories
    rows = []

    for item in results["detected_attacks"]:
        rows.append(flatten_entry(item["attack"], "Detected"))

    for item in results["missed_attacks"]:
        rows.append(flatten_entry(item, "Missed"))

    for item in results["false_positives"]:
        rows.append(flatten_entry(item, "False Positive"))

    # Convert to DataFrame
    if rows:
        df = pd.DataFrame(rows)
        df = df.reset_index(drop=True)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No results to display.")

    # Optional: auto-refresh
    if st.session_state.get('active_tab', '') == "Purple Team Analysis":
        time.sleep(2)
        st.experimental_rerun()

with blue_tab:
    st.header("Blue Team (Defense)")

    st.write("### ❌ Missed Attacks")
    if results["missed_attacks"]:
        for missed_attack in results["missed_attacks"]:
            st.json(missed_attack)
            recommendation = ai.recommend_solution(missed_attack, issue_type="missed_attack")
            st.write(f"**AI Recommendation:** {recommendation}")
    else:
        st.write("No missed attacks detected.")

    st.markdown("---")

    st.write("### ⚠️ False Positives")
    if results["false_positives"]:
        for false_positive in results["false_positives"]:
            st.json(false_positive)
            recommendation = ai.recommend_solution(false_positive, issue_type="false_positive")
            st.write(f"**AI Recommendation:** {recommendation}")
    else:
        st.write("No false positives detected.")

    if not results["missed_attacks"] and not results["false_positives"]:
        st.success("✅ No recommendations needed! Everything looks clean.")