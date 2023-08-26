import boto3

class DynamoDBStorage:
    def __init__(self, table_name, aws_region):
        self.table_name = table_name
        self.aws_region = aws_region
        self.dynamodb = boto3.resource('dynamodb', region_name=aws_region)
        self.table = self.dynamodb.Table(table_name)

    def set_state(self, chat_id, user_id, state, username=None):
        self.table.put_item(
            Item={
                'chat_id': chat_id,
                'user_id': user_id,
                'user_timestamp': state.get('user_timestamp'),
                'language': state.get('language'),
                'restaurant': state.get('restaurant'),
                'BotRunning': state.get('BotRunning', False),  # Default to False if not provided
                'username': username                           # Include the username field
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
                'BotRunning': item.get('BotRunning', False),  # Default to False if not present
                'username': item.get('username')  # Include the username field
            }
        return None

    # Other methods (set_data, get_data, delete) go here
