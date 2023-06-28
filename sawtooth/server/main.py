from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError

from families.controller_family import ControllerTransactionHandler
from families.record_family import RecordTransactionHandler
import traceback
import sys

def main():
    print('Servidor iniciou')
    try:
        processor = TransactionProcessor(url='tcp://validator:4004')
        controller_handler = ControllerTransactionHandler()
        record_handler = RecordTransactionHandler()
        processor.add_handler(controller_handler)
        processor.add_handler(record_handler)
        processor.start()
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

main()