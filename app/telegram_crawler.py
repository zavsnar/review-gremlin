import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your own values from https://my.telegram.org/apps
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')
SESSION_NAME = "telegram_session"

# Replace with the username or ID of the target channel
TARGET_CHANNEL = 'if_market_news' # e.g., 'durov' or -1001234567890


def load_data_to_chroma():
    """Loads data from MongoDB to ChromaDB."""
    print("Loading data from MongoDB to ChromaDB...")
    items = list(collection.find({}, {"_id": 0}))
    documents = [
        Document(page_content=item["text"], metadata={}) for item in items
    ]
    if documents:
        # Clear existing data in ChromaDB before loading
        try:
            chroma_client.reset_collection()
            print("Cleared existing ChromaDB collection.")
        except:
            print("No existing ChromaDB collection to clear.")
        
        chroma_client.add_documents(documents)
        print(f"Loaded {len(documents)} documents into ChromaDB.")

        results = chroma_client.similarity_search("tests")
        print(1111, results)
    else:
        print("No documents found in MongoDB to load into ChromaDB.")


async def get_channel_messages(channel_username, limit=100):
    """
    Connects to Telegram and fetches messages from a specific channel using Telethon.

    Args:
        channel_username (str): The username or ID of the channel.
        limit (int): The maximum number of messages to fetch.

    Returns:
        list: A list of message objects, or None if connection fails.
    """
    if not all([API_ID, API_HASH, PHONE_NUMBER]):
        print("Error: TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE_NUMBER must be set in .env file.")
        return None

    # Convert API_ID to integer
    try:
        api_id_int = int(API_ID)
    except ValueError:
        print("Error: TELEGRAM_API_ID must be an integer.")
        return None

    client = TelegramClient(SESSION_NAME, api_id_int, API_HASH)

    messages_data = []
    try:
        print("Connecting to Telegram...")
        await client.connect()

        if not await client.is_user_authorized():
            print("First run: Sending code request...")
            await client.send_code_request(PHONE_NUMBER)
            try:
                code = input('Enter the code you received: ')
                await client.sign_in(PHONE_NUMBER, code)
            except Exception as e:
                print(f"Failed to sign in: {e}")
                await client.disconnect()
                return None
            print("Signed in successfully!")

        print(f"Fetching messages from {channel_username}...")
        # Get the channel entity
        try:
            channel = await client.get_entity(channel_username)
        except ValueError:
             print(f"Error: Could not find the channel or chat with username/ID '{channel_username}'. Please check the username/ID.")
             await client.disconnect()
             return None
        except Exception as e:
            print(f"An unexpected error occurred while getting channel entity: {e}")
            await client.disconnect()
            return None


        # Fetch messages
        async for message in client.iter_messages(channel, limit=limit):
            # Process message object as needed
            # print(f"Message ID: {message.id}, Date: {message.date}, Text: {message.text[:50]}...")
            messages_data.append({
                'id': message.id,
                'date': message.date.isoformat(),
                'text': message.text,
                'sender_id': message.sender_id,
                # Add more fields as needed
            })
        print(f"Fetched {len(messages_data)} messages.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if client.is_connected():
            print("Disconnecting...")
            await client.disconnect()
            print("Disconnected.")

    return messages_data

async def main():
    """Main function to run the message fetching."""
    messages = await get_channel_messages(TARGET_CHANNEL, limit=10) # Fetch last 10 messages for testing
    if messages:
        print("\n--- Fetched Messages ---")
        for msg in messages:
            print(f"ID: {msg['id']}, Date: {msg['date']}, Sender: {msg['sender_id']}, Text: {msg['text'][:100]}...")
        print("----------------------\n")
    else:
        print("Failed to fetch messages.")

if __name__ == "__main__":
    # Use asyncio.run() in Python 3.7+
    # For older versions, you might need loop = asyncio.get_event_loop(); loop.run_until_complete(main())
    asyncio.run(main())