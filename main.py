from http.client import HTTPConnection
import jon
import time
from radom import randint
import rd
from pnput import keybard
import ting
from notypy import Notify

file = open("info.txt")
text = file.read().splitlines()

from datetime import datetime
start_time = datetime.now()
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

if len(text) != 5 or input("Configure bot? (y/n): ") == "y":
    file.close()
    file = open("info.txt", "w")
    text = []
    text.append(input("User agent: "))
    text.append(input("Discord token: "))
    text.append(input("Discord channel URL: "))
    text.append(input("Discord server ID: "))
    text.append(input("Discord channel ID: "))

    for parameter in text:
        file.write(parameter + "\n")

    file.close()

comm_file = open("dank_commands.txt")
command_list = comm_file.read().splitlines()

#with open("shop_items.json", "r") as f:
#    shop_item_dict = json.load(f)

with open("trivia_answers.json", "r") as f:
    trivia_answers_map = json.load(f)

header_data = {
    "content-type": "application/json",
    "user-agent": text[0],
    "authorization": text[1],
    "host": "discord.com",
    "referrer": text[2]
}

print("Messages will be sent to " + header_data["referrer"] + ".")


def connect():
    return HTTPSConnection("discord.com", 443)


def send_message(connection, channel_id, message):
    message_data = {
        "content": message,
        "tts": False  # tts stands for text-to-speech
    }

    try:
        connection.request("POST", f"/api/v9/channels/{channel_id}/messages", json.dumps(message_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300:  # everything is alright
            pass
        else:
            print(f"While sending message, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to send message")


def get_response(connection, channel_id):
    channel = connection.request("GET", f"/api/v9/channels/{channel_id}/messages", headers=header_data)
    response = connection.getresponse()

    if 199 < response.status < 300:  # everything is alright
        response_dict_str = response.read().decode('utf-8')
        response_dict = json.loads(response_dict_str)
        return response_dict
    else:
        print(f"While fetching message, received HTTP {response.status}: {response.reason}")


def reply_to_dank_memer(command):
    response_dict = get_response(connect(), text[4])

    if "search" in command:
        search_response(response_dict)
    elif "crime" in command:
        crime_response(response_dict)
    elif "pm" in command:
        pm_response(response_dict, 0)
    elif "hl" in command:
        hl_response(response_dict)
    elif "hunt" in command or "fish" in command or "dig" in command:
        hunt_fish_dig_response(response_dict)


def press_button(connection, channel_id, guild_id, message_id, button_id):
    button_data = {
        "type": 3,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_id": message_id,
        "message_flags": 0,
        "application_id": "270904126974590976",
        "session_id": "970dc09f57162d6469ff8448b72cfb2a",
        "data": {"component_type": 2, "custom_id": button_id}
    }

    try:
        connection.request("POST", "/api/v9/interactions", json.dumps(button_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300:  # everything is alright
            pass
        else:
            print(f"While pressing button, received HTTP {response.status}: {response.reason}")
    except:
        print("Failed to press button")


# separate search response to prioritise area51, grass, and mels room
def search_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        search_options = response_dict[0]["components"][0]["components"]
        option_labels = []
        #"soul's chamber", "aeradella's home", "kitchen", "dog", "grass", "god's own place", "phoenix pits", "fridge", "bed", "hospital", "shoe", "ca\
     #r", "vacuum", "garage", "basement", "pantry", "laundromat", "dresser", "mailbox", "washer", "sink", "sewer", "bus", "coat", "who asked", "pocket", "air", "a\
     #ttic", "bank", "bushes", "crawlspace", "dumpster", "couch", "glovebox", "purse", "uber", "van", "discord", "street", "tree", "area51"]
        for i in range(len(search_options)):
            option_labels.append(search_options[i]["label"])
        print(option_labels)
        if "soul's chamber" in option_labels:
            choice = search_options[option_labels.index("soul's chamber")]
        elif "aeradella's home" in option_labels:
            choice = search_options[option_labels.index("aeradella's home")]
        elif "kitchen" in option_labels:
            choice = search_options[option_labels.index("kitchen")]
        elif "dog" in option_labels:
            choice = search_options[option_labels.index("dog")]
        elif "god's own place" in option_labels:
            choice = search_options[option_labels.index("god's own place")]
        elif "phoenix pits" in option_labels:
            choice = search_options[option_labels.index("phoenix pits")]
        elif "hospital" in option_labels:
            choice = search_options[option_labels.index("hospital")]
        elif "air" in option_labels:
            choice = search_options[option_labels.index("air")]
        else:
            choice = search_options[randint(0, len(search_options) - 1)]
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"])
    except Exception as e:
        if len(response_dict[1]["components"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                search_response(response_dict[1:])
        print("Encountered exception during search:", e)


# separate crime response to prioritise tax evasion for badosz card
def crime_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        crime_options = response_dict[0]["components"][0]["components"]
        option_labels = []
        for i in range(len(crime_options)):
            option_labels.append(crime_options[i]["label"])
        if "tax evasion" in option_labels:
            choice = crime_options[option_labels.index("tax evasion")]
        else:
            choice = crime_options[randint(0, len(crime_options) - 1)]
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"])
    except Exception as e:
        if len(response_dict[1]["components"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                crime_response(response_dict[1:])
        print("Encountered exception during crime:", e)


def pm_response(response_dict, i):
    try:
        response = response_dict[i]["content"]
        if "need to buy" in response:
            send_message(connect(), text[4], "pls with 5000")
            time.sleep(2)
            send_message(connect(), text[4], "pls buy laptop")
        message_id = response_dict[i]["id"]
        pm_options = response_dict[i]["components"][0]["components"]
        choice = pm_options[randint(0, len(pm_options) - 1)]
        # now press the button
        press_button(connect(), text[4], text[3], message_id, choice["custom_id"])
        time.sleep(1)
        result_dict = get_response(connect(), text[4])
        result_msg = result_dict[i]["embeds"][0]["description"]
        if "broke" in result_msg:
            send_message(connect(), text[4], "pls item laptop")
            time.sleep(2)
            laptop_reply_dict = get_response(connect(), text[4])
            laptop_reply = laptop_reply_dict[0]["embeds"][0]["title"]
            if "owned" not in laptop_reply:
                send_message(connect(), text[4], "pls with 5000")
                time.sleep(1)
                send_message(connect(), text[4], "pls buy laptop")
    except Exception as e:
        if len(response_dict[1]["components"]) > 0 and len(response_dict[1]["embeds"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                pm_response(response_dict, 1)
        print("Encountered exception during postmemes:", e)


def hl_response(response_dict):
    try:
        message_id = response_dict[0]["id"]
        hint_message = response_dict[0]["embeds"][0]["description"]
        bold_asterisks = [a.start() for a in re.finditer("\*\*", hint_message)]
        hint_num = int(hint_message[(bold_asterisks[0] + 2):bold_asterisks[1]])
        if hint_num >= 50:
            low_button = response_dict[0]["components"][0]["components"][0]
            press_button(connect(), text[4], text[3], message_id, low_button["custom_id"])
        else:
            high_button = response_dict[0]["components"][0]["components"][2]
            press_button(connect(), text[4], text[3], message_id, high_button["custom_id"])
    except Exception as e:
        if len(response_dict[1]["components"]) > 0 and len(response_dict[1]["embeds"]) > 0:
            if "disabled" not in response_dict[1]["components"][0]["components"][0]:
                hl_response(response_dict[1:])
        print("Encountered exception during highlow:", e)


def hunt_fish_dig_response(response_dict):
    try:
        reply_content = response_dict[0]["content"]
        minigames = ["Dodge the Fireball", "Catch the fish", "order", "word", "game", "color", "Hit the ball",
                     "emoji"]
        if any(phrase in reply_content for phrase in minigames):
            print(reply_content)
            notification = Notify()
            notification.title = "THING HAPPENING"
            notification.message = "NEED HELP DRAGON OR FISH OR SOMETHING"
            notification.send()
    except Exception as e:
        print("Encountered exception during fish or dig:", e)


keep_running = True


def on_press(key):
    global keep_running
    if key == keyboard.Key.f9:
        print("Ok, time to stop.")
        keep_running = False
        return False


def main():
    '''#For testing
    send_message(connect(), text[4], "pls search")
    time.sleep(2)
    reply_to_dank_memer("pls search")
    time.sleep(randint(29, 35))
    '''
    beg_now = True #boolean
    while True:
        for command in command_list:
            if not keep_running:
                return
            command = command.split("=")[0].strip()
            if "beg" in command:
                if not beg_now:
                    beg_now = True
                    continue
                else:
                    beg_now = False
            send_message(connect(), text[4], command)
            if "dep" not in command or "beg" not in command:
                time.sleep(2)
                reply_to_dank_memer(command)  # sleep in this function, get the reply first
            time.sleep(2)


def press_event_button(connection, guild_id, channel_id, message_id, custom_id):
    button_data = {
        "type": 3,
        "guild_id": guild_id,
        "channel_id": channel_id,
        "message_id": message_id,
        "message_flags": 0,
        "application_id": "270904174590976",
        "session_id": "970dc09d6469ff8448b72cfb2a",
        "data": {"component_type": 2, "custom_id": custom_id}
    }

    try:
        connection.request("POST", "/api/v9/interactions", json.dumps(button_data), header_data)
        response = connection.getresponse()
        if 199 < response.status < 300:  # everything is alright
        else: #if you are seeing problems, this is your sign to GO LEARN HOW TO FUCKING CODE AND DO THIS SHIT ON YOUR OWN DUMBASS
            print(f"While pressing event button, received HTTP {response.status}: {response.reason}")
        print("Encountered exception when pressing event button:", e)


def capture_events():
    while True:
        if not keep_running:
            return
        global daily_duration, daily_count
        try:
            event_dict = get_response(connect(), text[4])
            message_id = event_dict[0]["id"]
            shop_sales = ["What is the **type**", "What is the **name**", "What is the **cost**"]

            if len(event_dict[0]["components"]) > 0 and len(
                    event_dict[0]["components"][0]["components"]) == 1:  # Boss fight
                print("Boss Event!")
                press_event_button(connect(), text[3], text[4], message_id,
                                   event_dict[0]["components"][0]["components"][0]["custom_id"])
            elif len(event_dict[0]["embeds"]) > 0 and len(event_dict[0]["components"]) > 0:
                event_embed = event_dict[0]["embeds"][0]
                embed_description = event_embed["description"]
                button_options = event_dict[0]["components"][0]["components"]
                if "chose a secret number" in embed_description:
                    hl_response(event_dict)
                elif "seconds to answer" in embed_description and "disabled" not in button_options[0]:
                    print("Trivia night boiiiiiiiiiiii")
                    button_options = event_dict[0]["components"][0]["components"]
                            if button["label"] == answer_text:
                                choice = button
                                break
                    else:
                        print("Can't find answer for trivia soz")
                        print(f"{text[2]}/{event_dict['id']}22
        except Exception as e:
            print("Encountered exception while capturing events:", e)


listener = keyboard.Listener(on_press=on_press)
listener.start()
main_thread = threading.Thread(target=main)
main_thread.start()
event_thread = threading.Thread(target=capture_events)
event_thread.start()
