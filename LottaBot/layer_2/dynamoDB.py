import boto3

class DynamoDBStorage:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_state(self, chat_id, user_id):
        response = self.table.get_item(Key={'chat_id': str(chat_id), 'user_id': str(user_id)})
        item = response.get('Item')
        if item:
            return item.get('state')
        return None

    def set_state(self, chat_id, user_id, state):
        self.table.put_item(Item={'chat_id': str(chat_id), 'user_id': str(user_id), 'state': state})

    def get_data(self, chat_id, user_id):
        response = self.table.get_item(Key={'chat_id': str(chat_id), 'user_id': str(user_id)})
        item = response.get('Item')
        if item:
            return item.get('data')
        return None

    def set_data(self, chat_id, user_id, data):
        self.table.put_item(Item={'chat_id': str(chat_id), 'user_id': str(user_id), 'data': data})

    def finish(self, chat_id, user_id):
        self.table.delete_item(Key={'chat_id': str(chat_id), 'user_id': str(user_id)})


# Create an instance of the DynamoDBStorage class
storage = DynamoDBStorage('Ruokabot')

# Set the state for a specific chat and user
chat_id = 123456789  # Replace with the actual chat ID
user_id = 987654321  # Replace with the actual user ID
state = 'some_state'  # Replace with the actual state value
storage.set_state(chat_id, user_id, state)