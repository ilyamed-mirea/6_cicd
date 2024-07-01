from app.models import Operation


class OperationsService:
    def create_operation(self):
        operation = Operation.objects.create()
        return operation

    def complete_operation(self, operation_id, result):
        try:
            operation = Operation.objects.get(id=operation_id)
            operation.completed = True
            operation.result = result
            operation.save()
            return operation
        except Operation.DoesNotExist:
            return None

    def finish_operation(self, operation_id):
        try:
            operation = Operation.objects.get(id=operation_id)
            operation.completed = True
            operation.save()
            return operation
        except Operation.DoesNotExist:
            return None

    def get_operation_info(self, operation_id):
        try:
            operation = Operation.objects.get(id=operation_id)
            return operation
        except Operation.DoesNotExist:
            return None
