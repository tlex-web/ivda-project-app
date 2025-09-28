import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class GroqClient:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"

    def _make_groq_request(
        self, company_name, prompt_file_path, max_tokens=150, temperature=0.7
    ):
        """Generic method to make Groq API requests"""
        if not self.api_key:
            return "Error: GROQ_API_KEY not found in environment variables"

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            # Load prompt file
            with open(prompt_file_path, "r") as file:
                messages_data = json.load(file)

            # Replace {company_name} in the prompt
            for message in messages_data["messages"]:
                message["content"] = message["content"].replace(
                    "{company_name}", company_name
                )

            # Make the API request
            response = requests.post(
                url,
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages_data["messages"],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                headers=headers,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"API Error: {response.status_code} - {response.text}"

        except FileNotFoundError:
            return f"Error: Prompt file not found at {prompt_file_path}"
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON in prompt file - {str(e)}"
        except requests.RequestException as e:
            return f"Error: Network request failed - {str(e)}"
        except KeyError as e:
            return f"Error: Unexpected response format - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_poem(self, company_name, prompt_file_path):
        """Generate a poem for the given company"""
        return self._make_groq_request(
            company_name, prompt_file_path, max_tokens=150, temperature=0.7
        )

    def generate_company_info(self, company_name, prompt_file_path):
        """Generate additional information for the given company"""
        return self._make_groq_request(
            company_name, prompt_file_path, max_tokens=200, temperature=0.3
        )
