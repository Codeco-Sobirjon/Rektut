from rest_framework.response import Response


def response_success(data: dict = None, status: int = 200) -> Response:
    """Returns a standardized successful response."""

    return Response(data={"success": True, "data": data}, status=status)


def response_error(data: dict = None, status: int = 400, message: str = "Ошибка") -> Response:
    """Returns a standardized unsuccessful response."""

    return Response(data={"success": False, "error_message": message, "data": data}, status=status)
