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
                'date': state.get('date'),
                'language': state.get('language'),
                'restaurant': state.get('restaurant')
            }
        )

    def get_state(self, chat_id, user_id):
        response = self.table.get_item(Key={'chat_id': chat_id, 'user_id': user_id})
        item = response.get('Item')
        if item:
            return {
                'date': item.get('date'),
                'language': item.get('language'),
                'restaurant': item.get('restaurant')
            }
        return None

    # Other methods (set_data, get_data, delete) go here

# Initialize DynamoDBStorage
storage = DynamoDBStorage("Ruokabot", "us-east-1")

# Set the state for a specific chat and user
# chat_id = "123456789"  # Replace with the actual chat ID
# user_id = "987654321"  # Replace with the actual user ID
# state = {
#     'date': '2023-08-25',
#     'language': 'en',
#     'restaurant': 'example_restaurant'
# }

# storage.set_state(chat_id, user_id, state)
