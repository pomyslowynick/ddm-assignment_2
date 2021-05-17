from better_profanity import profanity 
import json
def check_for_profanities(event, context):
  loaded_data = json.loads(event['data'])
  censored_text = {"censoredDescription": profanity.censor(loaded_data["description"])}
  return json.dumps(censored_text)