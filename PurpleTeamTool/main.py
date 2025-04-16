import streamlit as st
import purple
from red import red_team
from blue import blue_team
from mediator import AIModel
from log_manager import log_attack, log_detection, read_request, ATTACK_LOG_FILE, DETECTION_LOG_FILE
import time

ai = AIModel(api_key="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", model_name="mistralai/Mistral-7B-Instruct-v0.2")

# Title and Layout
st.title("Purple Team Security Tool")

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Red Team (Attack)"

tab_labels = ["Red Team (Attack)", "Custom Attacks", "Purple Team Analysis", "Blue Team (Defense)"]
tabs = st.tabs(tab_labels)
red_tab, custom_tab, purple_tab, blue_tab = tabs

# Streamlit workaround: session state active tab
for idx, label in enumerate(tab_labels):
    if tabs[idx]:
        st.session_state.active_tab = label

with red_tab:
    st.header("Red Team (Attack)")

    # Attack Buttons
    if st.button("Launch SQL Injection"):
        target = "http://testphp.vulnweb.com/login.php"
        output = red_team.sql_injection(target)
        st.text_area("Red Team Log", output, height=200)

    if st.button("Launch XSS Attack"):
        target = "http://testphp.vulnweb.com/login.php"
        output = red_team.xss_attack(target)
        st.text_area("Red Team Log", output, height=200)

    if st.button("Launch RCE Attack"):
        command = "whoami"
        output = red_team.rce_attack(command)
        st.text_area("Red Team Log", output, height=200)

with custom_tab:
    st.header("Custom Attacks")

    # Use a form to properly scope the inputs and buttons
    with st.form("custom_attack_form"):
        log_type = st.text_input("Attack Type (SQLi, XSS, RCE):")
        target_url = st.text_input("Target URL:")
        attack_details = st.text_area("Attack Details:")
        attacker_ip = st.text_input("Attacker IP (Optional)", value="ManualInput")
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
    
    st.markdown("---")
    st.header("Custom Defense Logging")

    with st.form("custom_defense_form"):
        detection_type = st.text_input("Detection Type (SQLi, XSS, RCE):", key="defense_type")
        target_url = st.text_input("Target URL:", key="defense_target")
        detected_input = st.text_area("Detected Input (Payload):")
        source_ip = st.text_input("Source IP (Optional):", value="ManualInput", key="source_ip")
        action_taken = st.text_input("Action Taken (Blocked, Alerted, etc.):")
        defense_submitted = st.form_submit_button("Log Detection")

        if defense_submitted:
            if not detection_type or not target_url or not detected_input or not action_taken:
                st.error("All fields must be filled out.")
            else:
                try:
                    log_detection(detection_type, target_url, detected_input, source_ip, action_taken)
                    st.success(f"[LOGGED] {detection_type} detection logged.")
                except Exception as e:
                    st.error(f"[ERROR] Failed to write detection log: {str(e)}")


with purple_tab:
    st.header("Purple Team Analysis")
    
    results = purple.run_purple_team_analysis(ATTACK_LOG_FILE, DETECTION_LOG_FILE)

    # Display the results
    st.write("### ✅ Detected Attacks")
    if results["detected_attacks"]:
        st.json(results["detected_attacks"])
    else:
        st.info("No detected attacks.")

    st.write("### ❌ Missed Attacks")
    if results["missed_attacks"]:
        st.json(results["missed_attacks"])
    else:
        st.success("No missed attacks!")

    st.write("### ⚠️ False Positives")
    if results["false_positives"]:
        st.json(results["false_positives"])
    else:
        st.success("No false positives!")
    
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