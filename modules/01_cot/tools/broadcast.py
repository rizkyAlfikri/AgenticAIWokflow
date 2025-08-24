from loguru import logger

def broadcast(message: str):
    logger.info(f"Broadcasting message: {message}")
    return f"Broadcasted message: {message}"

broadcast_def = {
    "type": "function",
    "function": {
        "name": "broadcast",
        "description": "Broadcast a message to all connected clients.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to broadcast.",
                },
            },
            "required": ["message"],
        },
    },  
}