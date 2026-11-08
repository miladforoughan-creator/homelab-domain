from foodbot_loader import FoodBot
from email_manager import EmailManager
import json
from gemini_manager import GeminiManager
from dotenv import load_dotenv

load_dotenv()

RECIPIENT1 = os.environ.get("RECIPIENT1)
RECIPIENT2 = os.environ.get("RECIPIENT2)

food_bot = FoodBot()
food_bot_data = food_bot.get_sheet_data()
print(food_bot_data)
latest_item = food_bot_data["foodForm"][-1]
food_profile_dict = {
    "ingredients" : latest_item["ingredients"],
    "duration" : latest_item["duration"],
    "portions" : latest_item["people"],
}
print(food_profile_dict)
food_profile = json.dumps(food_profile_dict, indent=4)

with open("gemini_food_prompt.txt", "r") as file:
    prompt = file.read()

gemini = GeminiManager(35000, 1,1, models=["gemini-3.6-flash"])
gemini_response = gemini.generate_response(prompt)

email = EmailManager()
recipient = [RECIPIENT1, RECIPIENT2]
subject = "Food Recommendation"
html_content = gemini_response
email.send_email(recipient,
                 subject,
                 html_content
)
