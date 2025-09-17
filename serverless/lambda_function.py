import json, os, uuid, boto3
TABLE = os.environ.get("TABLE_NAME", "")
dynamo = boto3.resource('dynamodb').Table(TABLE)

def handler(event, context):
    body = json.loads(event.get('body') or "{}")
    item = {
        "id": str(uuid.uuid4()),
        "payload": body
    }
    dynamo.put_item(Item=item)
    return {
        "statusCode": 200,
        "headers": {"Content-Type":"application/json"},
        "body": json.dumps({"ok": True, "id": item["id"]})
    }
