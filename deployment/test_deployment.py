"""Interactive test script for deployed Trade Agent on Vertex AI Agent Engine."""

import os

import vertexai
from absl import app, flags
from dotenv import load_dotenv
from vertexai import agent_engines

FLAGS = flags.FLAGS

flags.DEFINE_string("project_id", None, "GCP project ID.")
flags.DEFINE_string("location", None, "GCP location.")
flags.DEFINE_string("bucket", None, "GCP bucket.")
flags.DEFINE_string(
    "resource_id",
    None,
    "ReasoningEngine resource ID (returned after deploying the agent).",
)
flags.DEFINE_string("user_id", None, "User ID (can be any string).")
flags.mark_flag_as_required("resource_id")
flags.mark_flag_as_required("user_id")


def main(argv: list[str]) -> None:
    del argv  # unused
    load_dotenv()

    project_id = (
        FLAGS.project_id if FLAGS.project_id else os.getenv("GOOGLE_CLOUD_PROJECT")
    )
    location = (
        FLAGS.location if FLAGS.location else os.getenv("GOOGLE_CLOUD_LOCATION")
    )
    bucket = (
        FLAGS.bucket if FLAGS.bucket else os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    )

    if not project_id:
        print("Missing required environment variable: GOOGLE_CLOUD_PROJECT")
        return
    elif not location:
        print("Missing required environment variable: GOOGLE_CLOUD_LOCATION")
        return
    elif not bucket:
        print("Missing required environment variable: GOOGLE_CLOUD_STORAGE_BUCKET")
        return

    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=f"gs://{bucket}",
    )

    agent = agent_engines.get(FLAGS.resource_id)
    print(f"Found agent with resource ID: {FLAGS.resource_id}")
    session = agent.create_session(user_id=FLAGS.user_id)
    print(f"Created session for user ID: {FLAGS.user_id}")
    print("Type 'quit' to exit.\n")
    print("Example queries:")
    print("  - How is my portfolio doing?")
    print("  - Any urgent options actions?")
    print("  - What do you think of AAPL?")
    print("  - Analyze my TSLA position\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        for event in agent.stream_query(
            user_id=FLAGS.user_id,
            session_id=session["id"],
            message=user_input,
        ):
            if "content" in event:
                if "parts" in event["content"]:
                    parts = event["content"]["parts"]
                    for part in parts:
                        if "text" in part:
                            print(f"Agent: {part['text']}")

    agent.delete_session(user_id=FLAGS.user_id, session_id=session["id"])
    print(f"\nSession ended for user ID: {FLAGS.user_id}")


if __name__ == "__main__":
    app.run(main)
