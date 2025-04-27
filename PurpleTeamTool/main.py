import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import purple
from red import run_payload
from mediator import AIModel
from log_manager import log_attack, ATTACK_LOG_FILE, DETECTION_LOG_FILE
import time

ai = AIModel(api_key="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", model_name="mistralai/Mixtral-8x7B-Instruct-v0.1")

USER_CREDENTIALS = {
    "admin": {"password": "adminpass", "role": "admin"},
    "red": {"password": "redpass", "role": "red"},
    "blue": {"password": "bluepass", "role": "blue"}
}

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_role'] = None

if not st.session_state['logged_in']:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = USER_CREDENTIALS.get(username)
        if user and user["password"] == password:
            st.session_state['logged_in'] = True
            st.session_state['user_role'] = user["role"]
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials.")
else:
    role = st.session_state['user_role']

    st.markdown("""
        <style>
            .block-container {
                max-width: 95vw !important;
                padding-left: 20rem !important;
                padding-right: 20rem !important;
            }
        </style>
        """, unsafe_allow_html=True)

    st.title("Purple Team Security Tool")

    # Define tab visibility based on user role
    tabs_dict = {
        "admin": ["Red Team (Attack)", "Custom Attack Logging", "Purple Team Analysis", "Blue Team (Defense)"],
        "red": ["Red Team (Attack)", "Custom Attack Logging", "Purple Team Analysis"],
        "blue": ["Purple Team Analysis", "Blue Team (Defense)"]
    }

    tabs_labels = tabs_dict[role]
    tabs = st.tabs(tabs_labels)

    tabs_content = {label: tab for label, tab in zip(tabs_labels, tabs)}

    if "Red Team (Attack)" in tabs_content:
        with tabs_content["Red Team (Attack)"]:
            st.header("Red Team (Attack)")

            with st.expander("Configure Target IP"):
                target_ip = st.text_input("Enter Target IP", value="192.168.8.133")

            if st.button("Basic SQL Injection"):
                red_team_payload = f'curl -i "http://{target_ip}/index.html?user=admin%27%20OR%201%3D1--"'
                result = run_payload(red_team_payload, "SQLi")
                st.text_area("Red Team Log", result, height=200)

            if st.button("Basic XSS"):
                red_team_payload = f'curl -i "http://{target_ip}/index.html?q=<script>alert(\'XSS\')</script>"'
                result = run_payload(red_team_payload, "XSS")
                st.text_area("Red Team Log", result, height=200)

            if st.button("Command Injection"):
                red_team_payload = f'curl -i -X POST "http://{target_ip}/login" -d "username=admin;phpinfo();" -A "curl"'
                result = run_payload(red_team_payload, "CMDi")
                st.text_area("Red Team Log", result, height=200)

            if st.button("Basic LFI"):
                red_team_payload = f'curl -i "http://{target_ip}/index.html?page=../../../../etc/passwd"'
                result = run_payload(red_team_payload, "LFI")
                st.text_area("Red Team Log", result, height=200)

            if st.button("False Positive - SQL Keyword"):
                red_team_payload = f'curl -i "http://{target_ip}/index.html?contact=%22+SELECT+FROM+help"'
                result = run_payload(red_team_payload, "False Positive")
                st.text_area("Red Team Log", result, height=200)

    if "Custom Attack Logging" in tabs_content:
        with tabs_content["Custom Attack Logging"]:
            st.header("Custom Attacks")

            with st.form("custom_attack_form"):
                log_type = st.text_input("Attack Type (SQLi, XSS, RCE):")
                target_url = st.text_input("Target:", value="192.168.8.133")
                attack_details = st.text_area("Attack Details:")
                attacker_ip = st.text_input("Attacker IP:", value="192.168.8.157")
                submitted = st.form_submit_button("Log Attack")

                if submitted:
                    if not log_type or not target_url or not attack_details:
                        st.error("All fields must be filled out.")
                    else:
                        try:
                            log_attack(log_type, target_url, attack_details, attacker_ip)
                            st.success(f"[LOGGED] {log_type} attack on {target_url}")
                        except Exception as e:
                            st.error(f"[ERROR] Failed to write log: {str(e)}")

    if "Purple Team Analysis" in tabs_content:
        with tabs_content["Purple Team Analysis"]:

            results = purple.run_purple_team_analysis(ATTACK_LOG_FILE, DETECTION_LOG_FILE)

            detected = len(results["detected_attacks"])
            missed = len(results["missed_attacks"])
            false_positives = len(results["false_positives"])

            total = detected + missed + false_positives

            if total > 0:
                labels = ['Detected', 'Missed', 'False Positive']
                sizes = [detected, missed, false_positives]
                colors = ['#3498db', '#8e44ad', '#e0e0e0']  # blue, purple, pale gray
                
                # Create smaller figure
                fig, ax = plt.subplots(figsize=(4, 4), dpi=600, facecolor='none')  # smaller size, higher DPI

                wedges, _texts = ax.pie(
                    sizes,
                    labels=None,
                    autopct=None,  # Disable percentage text
                    colors=colors,
                    startangle=120,
                    textprops={'color': 'black', 'fontsize': 7}
                )

                fig.patch.set_alpha(0.0)
                ax.patch.set_alpha(0.0)

                # Add clean manual labels inside the slices
                for i, wedge in enumerate(wedges):
                    angle = (wedge.theta2 + wedge.theta1) / 2
                    x = 0.5 * np.cos(np.deg2rad(angle))
                    y = 0.5 * np.sin(np.deg2rad(angle))
                    label_text = f"{labels[i]}\n{sizes[i]/total*100:.1f}%"  # show label + percent
                    ax.text(x, y, label_text, ha='center', va='center', fontsize=10, color='black')

                ax.axis('equal')  # Force circle

                # ✅ Save the figure to an in-memory buffer
                buf = io.BytesIO()
                fig.savefig(buf, format="png", bbox_inches="tight", transparent=True, dpi=600)
                buf.seek(0)

                # ✅ Use columns to center
                col1, col2, col3 = st.columns([1,1,1])

                with col2:
                    st.image(buf, width=500)
            else:
                st.info("No attack data available for visualization.")
                
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
                st.rerun()

    if "Blue Team (Defense)" in tabs_content:
        with tabs_content["Blue Team (Defense)"]:

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
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['user_role'] = None
        st.rerun()