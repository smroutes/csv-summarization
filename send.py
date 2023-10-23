import constants
from utils import sendMessage

inputPrompt = {
    'fileName': 'feedback.csv',
    'columnName': 'What could be improved about this session?',
    'modelName': 'flant5base'
}

sendMessage(inputPrompt, constants.ROUTING_INPUT_QUEUE);
