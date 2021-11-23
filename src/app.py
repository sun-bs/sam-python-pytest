import json
from sub_app import return_value
from custom_exception import CustomException
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    try:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': return_value()
            })
        }
    except CustomException:
        logger.info('CustomExceptionをキャッチ')
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'bad request'
            })
        }
    except Exception as e:
        logger.info(f'{e.__class__.__name__}をキャッチ')
        raise e
