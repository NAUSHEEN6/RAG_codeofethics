import sys
from pathlib import Path
import json

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st

from app.orchestrator import answer_ethics_question
from mcp_integration.client import run_tool


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ethics Copilot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "case_result" not in st.session_state:
    st.session_state.case_result = None

if "case_data" not in st.session_state:
    st.session_state.case_data = None

if "report_result" not in st.session_state:
    st.session_state.report_result = None

if "report_data" not in st.session_state:
    st.session_state.report_data = None

if "email_result" not in st.session_state:
    st.session_state.email_result = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_mcp_json(mcp_result):
    """
    Extract JSON data from an MCP CallToolResult.
    """

    try:

        if hasattr(mcp_result, "content"):

            for item in mcp_result.content:

                if hasattr(item, "text"):

                    return json.loads(item.text)

    except Exception:
        pass

    return None


def extract_report(mcp_result):
    """
    Extract the actual generated report text
    from the MCP create_report response.
    """

    data = extract_mcp_json(mcp_result)

    if data and "report" in data:
        return data["report"]

    return ""


# ============================================================
# HEADER
# ============================================================

st.title("⚖️ Ethics Copilot")

st.caption(
    "AI-assisted Code of Business Ethics guidance "
    "using Retrieval-Augmented Generation, Gemini, "
    "MCP and Outlook"
)

st.divider()


# ============================================================
# QUESTION INPUT
# ============================================================

st.subheader("Ask an Ethics Question")

question = st.text_area(
    "Describe your situation",
    placeholder=(
        "Example:\n"
        "A supplier offered me an expensive gift. "
        "Could this create a conflict of interest "
        "and what should I do?"
    ),
    height=140
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🔍 Analyze Ethics Question",
    type="primary",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter an ethics question."
        )

    else:

        # Reset previous workflow
        st.session_state.case_result = None
        st.session_state.case_data = None
        st.session_state.report_result = None
        st.session_state.report_data = None
        st.session_state.email_result = None

        with st.spinner(
            "Searching the Code of Business Ethics and "
            "generating an assessment..."
        ):

            try:

                analysis = answer_ethics_question(
                    question.strip()
                )

                st.session_state.analysis = analysis

            except Exception as e:

                st.error(
                    f"Analysis failed: {e}"
                )


# ============================================================
# DISPLAY ANALYSIS
# ============================================================

if st.session_state.analysis:

    result = st.session_state.analysis

    st.divider()

    # ========================================================
    # AI ASSESSMENT
    # ========================================================

    st.subheader("🧠 Ethics Assessment")

    st.info(
        result["answer"]
    )


    # ========================================================
    # POLICY EVIDENCE
    # ========================================================

    st.subheader(
        "📚 Retrieved Policy Evidence"
    )

    sources = result.get(
        "sources",
        []
    )

    if sources:

        for index, source in enumerate(
            sources,
            start=1
        ):

            page = source.get(
                "page",
                "N/A"
            )

            section = source.get(
                "section",
                "Policy"
            )

            with st.expander(
                f"Source {index} — Page {page} — {section}"
            ):

                st.write(
                    source.get(
                        "text",
                        ""
                    )
                )

                if "distance" in source:

                    st.caption(
                        f"Retrieval distance: "
                        f"{source['distance']:.4f}"
                    )

    else:

        st.warning(
            "No policy sources were returned."
        )


    # ========================================================
    # CASE MANAGEMENT
    # ========================================================

    st.divider()

    st.subheader(
        "⚙️ Ethics Case Management"
    )

    if st.session_state.case_result is None:

        st.write(
            "Create a structured ethics case from "
            "this assessment."
        )

        if st.button(
            "📝 Create Ethics Case",
            use_container_width=True
        ):

            if not sources:

                st.error(
                    "Cannot create a case because "
                    "no policy source was retrieved."
                )

            else:

                best_source = sources[0]

                with st.spinner(
                    "Creating ethics case through MCP..."
                ):

                    try:

                        case_result = run_tool(
                            "create_case",
                            {
                                "employee_question":
                                    question.strip(),

                                "policy_section":
                                    best_source.get(
                                        "section",
                                        "Code of Business Ethics"
                                    ),

                                "policy_page":
                                    int(
                                        best_source.get(
                                            "page",
                                            0
                                        )
                                    ),

                                "assessment":
                                    result["answer"]
                            }
                        )

                        st.session_state.case_result = (
                            case_result
                        )

                        case_data = extract_mcp_json(
                            case_result
                        )

                        st.session_state.case_data = (
                            case_data
                        )

                        st.success(
                            "✅ Ethics case created successfully "
                            "through MCP."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Case creation failed: {e}"
                        )


    # ========================================================
    # CASE RESULT
    # ========================================================

    if st.session_state.case_data:

        case_data = st.session_state.case_data

        st.success(
            f"Case created: "
            f"**{case_data.get('case_id', 'N/A')}**"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Case ID",
                case_data.get(
                    "case_id",
                    "N/A"
                )
            )

        with col2:

            st.metric(
                "Status",
                case_data.get(
                    "status",
                    "OPEN"
                )
            )

        with col3:

            st.metric(
                "Policy Page",
                case_data.get(
                    "policy_page",
                    "N/A"
                )
            )


    # ========================================================
    # REPORT GENERATION
    # ========================================================

    if st.session_state.case_data:

        st.divider()

        st.subheader(
            "📄 Ethics Case Report"
        )

        case_id = st.session_state.case_data.get(
            "case_id"
        )

        if not st.session_state.report_data:

            st.write(
                "Generate the official case report "
                "from the stored ethics case."
            )

            if st.button(
                "📄 Generate Ethics Report",
                use_container_width=True
            ):

                with st.spinner(
                    "Generating ethics report through MCP..."
                ):

                    try:

                        report_result = run_tool(
                            "create_report",
                            {
                                "case_id": case_id
                            }
                        )

                        st.session_state.report_result = (
                            report_result
                        )

                        report_data = extract_mcp_json(
                            report_result
                        )

                        st.session_state.report_data = (
                            report_data
                        )

                        st.success(
                            "✅ Ethics report generated successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Report generation failed: {e}"
                        )


    # ========================================================
    # DISPLAY ACTUAL REPORT
    # ========================================================

    if st.session_state.report_data:

        report_data = (
            st.session_state.report_data
        )

        report_text = report_data.get(
            "report",
            ""
        )

        report_file = report_data.get(
            "file",
            ""
        )

        if report_text:

            st.success(
                "✅ Report generated"
            )

            # ------------------------------------------------
            # THIS IS THE ACTUAL REPORT
            # ------------------------------------------------

            st.text_area(
                "Generated Ethics Report",
                value=report_text,
                height=400,
                disabled=True
            )

            if report_file:

                st.caption(
                    f"Saved locally: {report_file}"
                )

        else:

            st.error(
                "The MCP report tool did not return "
                "the actual report content."
            )


    # ========================================================
    # OUTLOOK EMAIL
    # ========================================================

    if (
        st.session_state.report_data
        and st.session_state.report_data.get("report")
    ):

        st.divider()

        st.subheader(
            "📧 Prepare Report in Outlook"
        )

        st.info(
            "The exact report displayed above will be "
            "used as the email body. Review the recipient "
            "and report before sending."
        )

        recipient = st.text_input(
            "Recipient email address",
            placeholder="ethics-team@company.com"
        )

        confirm = st.checkbox(
            "I confirm that I have reviewed the report and want to prepare it for sending."
        )

        if st.button(
            "📤 Prepare Email in Outlook",
            type="primary",
            use_container_width=True
        ):

            if not recipient.strip():

                st.warning(
                    "Please enter a recipient email address."
                )

            elif not confirm:

                st.warning(
                    "Please confirm that you reviewed "
                    "the report before preparing the email."
                )

            else:

                # =================================================
                # IMPORTANT:
                # USE THE EXACT SAME REPORT GENERATED BY MCP
                # =================================================

                email_body = report_data["report"]

                with st.spinner(
                    "Preparing the ethics report in Outlook..."
                ):

                    try:

                        email_result = run_tool(
                            "send_email",
                            {
                                "recipient":
                                    recipient.strip(),

                                "subject":
                                    (
                                        f"Ethics Copilot - "
                                        f"Case {case_id} Report"
                                    ),

                                "body":
                                    email_body
                            }
                        )

                        st.session_state.email_result = (
                            email_result
                        )

                        email_data = extract_mcp_json(
                            email_result
                        )

                        if (
                            email_data
                            and email_data.get("success")
                        ):

                            st.success(
                                "📧 Email prepared in Outlook successfully."
                            )

                            st.caption(
                                "Please review the recipient and "
                                "report in Outlook before clicking Send."
                            )

                        else:

                            st.error(
                                "The email tool did not complete successfully."
                            )

                            st.write(
                                email_result
                            )

                    except Exception as e:

                        st.error(
                            f"Outlook preparation failed: {e}"
                        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "⚖️ Ethics Copilot provides AI-assisted guidance "
    "based on retrieved Code of Business Ethics content. "
    "It does not replace advice from Ethics, Compliance, "
    "HR or Legal functions."
)