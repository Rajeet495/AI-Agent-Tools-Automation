import streamlit as st
from groq import Groq
import json

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Agent with Tools & Memory",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# GROQ CLIENT
# --------------------------------------------------

groq_api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=groq_api_key)

MODEL = "openai/gpt-oss-20b"

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "activity" not in st.session_state:
    st.session_state.activity = []

# --------------------------------------------------
# TOOLS
# --------------------------------------------------

def calculator(a, b, operation):
    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero."
        return a / b

    return "Unknown operation."


def get_text_length(text):
    return len(text)


# --------------------------------------------------
# TOOL DEFINITIONS
# --------------------------------------------------

tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform a mathematical calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "Mathematical operation"
                    }
                },
                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_text_length",
            "description": "Count the number of characters in a text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text whose characters should be counted."
                    }
                },
                "required": ["text"]
            }
        }
    }
]

# --------------------------------------------------
# SAFETY VALIDATION
# --------------------------------------------------

ALLOWED_TOOLS = {
    "calculator",
    "get_text_length"
}


def validate_tool(tool_name, arguments):

    if tool_name not in ALLOWED_TOOLS:
        return False, "Tool is not allowed."

    # Calculator validation
    if tool_name == "calculator":

        if "a" not in arguments:
            return False, "Missing first number."

        if "b" not in arguments:
            return False, "Missing second number."

        if "operation" not in arguments:
            return False, "Missing operation."

        if arguments["operation"] not in [
            "add",
            "subtract",
            "multiply",
            "divide"
        ]:
            return False, "Invalid operation."

        if not isinstance(
            arguments["a"],
            (int, float)
        ):
            return False, "First number must be numeric."

        if not isinstance(
            arguments["b"],
            (int, float)
        ):
            return False, "Second number must be numeric."

        if (
            arguments["operation"] == "divide"
            and arguments["b"] == 0
        ):
            return False, "Division by zero is not allowed."

    # Text length validation
    elif tool_name == "get_text_length":

        if "text" not in arguments:
            return False, "Missing text."

        if not isinstance(
            arguments["text"],
            str
        ):
            return False, "Text must be a string."

    return True, "Safety validation passed."


# --------------------------------------------------
# TOOL EXECUTION
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name == "calculator":
        return calculator(**arguments)

    elif tool_name == "get_text_length":
        return get_text_length(**arguments)

    return "Unknown tool."


# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("🤖 AI Agent with Tools & Memory")

st.write(
    "A Groq-powered AI agent with tool calling, "
    "conversation memory, state tracking, "
    "multi-tool execution, and safety validation."
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("🧠 Agent State")

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    st.metric(
        "Tool Actions",
        len(st.session_state.activity)
    )

    st.divider()

    st.subheader("🔧 Available Tools")

    st.write("• Calculator")
    st.write("• Text Length")

    st.divider()

    if st.button("Clear Conversation"):

        st.session_state.messages = []
        st.session_state.activity = []

        st.rerun()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    if message["role"] in [
        "user",
        "assistant"
    ]:

        with st.chat_message(
            message["role"]
        ):
            st.write(
                message["content"]
            )


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_request = st.chat_input(
    "Ask the AI Agent something..."
)


if user_request:

    # ----------------------------------------------
    # ADD USER MESSAGE TO MEMORY
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_request
        }
    )

    with st.chat_message("user"):
        st.write(user_request)

    try:

        # ------------------------------------------
        # FIRST LLM CALL
        # ------------------------------------------

        response = client.chat.completions.create(
            model=MODEL,
            messages=st.session_state.messages,
            tools=tool_definitions,
            tool_choice="auto"
        )

        assistant_message = (
            response.choices[0].message
        )

        # ------------------------------------------
        # NO TOOL REQUIRED
        # ------------------------------------------

        if not assistant_message.tool_calls:

            answer = assistant_message.content

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.chat_message("assistant"):
                st.write(answer)

        # ------------------------------------------
        # TOOL CALLS REQUIRED
        # ------------------------------------------

        else:

            # Store assistant tool-call message
            assistant_message_dict = {
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": []
            }

            for tool_call in assistant_message.tool_calls:

                assistant_message_dict[
                    "tool_calls"
                ].append(
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }
                )

            st.session_state.messages.append(
                assistant_message_dict
            )

            # --------------------------------------
            # EXECUTE ALL TOOL CALLS
            # --------------------------------------

            for tool_call in assistant_message.tool_calls:

                tool_name = (
                    tool_call.function.name
                )

                arguments = json.loads(
                    tool_call.function.arguments
                )

                # Safety validation
                is_valid, safety_message = (
                    validate_tool(
                        tool_name,
                        arguments
                    )
                )

                if not is_valid:

                    tool_result = (
                        f"Safety blocked: "
                        f"{safety_message}"
                    )

                    st.session_state.activity.append(
                        {
                            "tool": tool_name,
                            "status": "BLOCKED",
                            "arguments": arguments,
                            "result": tool_result
                        }
                    )

                else:

                    # Execute tool
                    tool_result = execute_tool(
                        tool_name,
                        arguments
                    )

                    st.session_state.activity.append(
                        {
                            "tool": tool_name,
                            "status": "SUCCESS",
                            "arguments": arguments,
                            "result": tool_result
                        }
                    )

                # ----------------------------------
                # SAVE TOOL RESULT TO MEMORY
                # ----------------------------------

                st.session_state.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_result)
                    }
                )

            # --------------------------------------
            # SECOND LLM CALL
            # Uses COMPLETE conversation history
            # --------------------------------------

            final_response = (
                client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages,
                    tools=tool_definitions
                )
            )

            final_message = (
                final_response
                .choices[0]
                .message
            )

            answer = (
                final_message.content
                or "The tool action was completed."
            )

            # --------------------------------------
            # SAVE FINAL RESPONSE TO MEMORY
            # --------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.chat_message("assistant"):

                st.write(answer)

                tool_names = [
                    call.function.name
                    for call in assistant_message.tool_calls
                ]

                st.caption(
                    "🔧 Tools used: "
                    + ", ".join(tool_names)
                )

    except Exception as e:

        with st.chat_message("assistant"):

            st.error(
                f"An error occurred: {str(e)}"
            )


# --------------------------------------------------
# AGENT ACTIVITY
# --------------------------------------------------

if st.session_state.activity:

    st.divider()

    st.subheader("🔍 Agent Activity")

    for i, activity in enumerate(
        st.session_state.activity,
        start=1
    ):

        with st.expander(
            f"Action {i}: {activity['tool']}"
        ):

            st.write(
                "Status:",
                activity["status"]
            )

            st.write("Arguments:")

            st.json(
                activity["arguments"]
            )

            if "result" in activity:

                st.write(
                    "Result:",
                    activity["result"]
                )