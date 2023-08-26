import boto3

class DynamoDBStorage:
    def __init__(self, table_name, aws_region):
        self.table_name = table_name
        self.aws_region = aws_region
        self.dynamodb = boto3.resource('dynamodb', region_name=aws_region)
        self.table = self.dynamodb.Table(table_name)

    def set_state(self, chat_id, user_id, state):
        self.table.put_item(
            Item={
                'chat_id': chat_id,
                'user_id': user_id,
                'user_timestamp': state.get('user_timestamp'),
                'language': state.get('language'),
                'restaurant': state.get('restaurant'),
                'BotRunning': state.get('BotRunning', False)  # Default to False if not provided
            }
        )

    def get_state(self, chat_id, user_id):
        response = self.table.get_item(Key={'chat_id': chat_id, 'user_id': user_id})
        item = response.get('Item')
        if item:
            return {
                'user_timestamp': item.get('user_timestamp'),
                'language': item.get('language'),
                'restaurant': item.get('restaurant'),
                'BotRunning': item.get('BotRunning', False)  # Default to False if not present
            }
        return None

    # Other methods (set_data, get_data, delete) go here

# Initialize DynamoDBStorage
# storage = DynamoDBStorage("Ruokabot", "us-east-1")

# Example usage:
# chat_id = "123456789"
# user_id = "987654321"
# state = {
#     'user_timestamp': '2023-08-25 12:34:56',
#     'language': 'en',
#     'restaurant': 'example_restaurant',
#     'BotRunning': True  # You can set this value based on your use case
# }

# storage.set_state(chat_id, user_id, state)
