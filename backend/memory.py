conversation_memory = {}

def save_memory(key, value):
    conversation_memory[key] = value

def set_active_field(field):
    conversation_memory["active_field"] = field

def get_active_field():
    return conversation_memory.get("active_field")

def clear_active_field():
    conversation_memory.pop("active_field", None)

def get_memory():
    return conversation_memory

def clear_memory():
    conversation_memory.clear()

def set_confirmation_pending():
    conversation_memory["confirmation_pending"] = True

def clear_confirmation_pending():
    conversation_memory.pop("confirmation_pending", None)