#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from crew import Mongo_Reccomender
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    print("🤖 CrewAI Supervisor is ready.")
    user_input = input("🗣️ You: ")
    inputs = {
        'user_name': 'Sai Krish',
        'user_message': user_input, 
        # 'Hey, can you recommend some products for me based on my purchase history? My user name is Sai Krish.'
    }
    try:
        result = Mongo_Reccomender().crew().kickoff(
            inputs=inputs
        )
        print("\n✅ Final Output:\n", result)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    finally:
        # Ensure that the MongoDB adapter is stopped to avoid resource leaks
        Mongo_Reccomender().mongo_adapter.stop()


run()
