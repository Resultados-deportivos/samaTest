flash_messages = []

# Add this code to your views.py
def add_flash_message(message, category):
    flash_messages.append((message, category))

def get_flash_messages():
    global flash_messages
    messages = flash_messages
    flash_messages = []  # Clear flash messages after retrieving
    return messages
