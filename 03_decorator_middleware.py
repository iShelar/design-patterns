from abc import ABC, abstractmethod


class Handler(ABC):

    @abstractmethod
    def handle(self, request: str) -> str:
        ...


class Middleware(Handler):

    def __init__(self, handler: Handler) -> None:
        self.handler = handler


class Application(Handler):

    def handle(self, request: str) -> str:
        return f"Application handled: {request}"


class LoggingMiddleware(Middleware):

    def handle(self, request: str) -> str:
        print(f"Logging: received {request}")

        response = self.handler.handle(request)

        print(f"Logging: response = {response}")

        return response


class AuthenticationMiddleware(Middleware):

    def handle(self, request: str) -> str:
        print("Authentication: checking request")
        if "token" not in request:
            return "401 Unauthorized"

        response = self.handler.handle(request)

        return response

print("---------- Application ----------")

app = Application()
print(app.handle("GET /users"))


print("---------- Authentication ----------")

auth = AuthenticationMiddleware(Application())
print(auth.handle("GET /users"))
print(auth.handle("GET /users token"))


print("---------- Logging ----------")

log = LoggingMiddleware(Application())
print(log.handle("GET /users token"))


print("---------- Authentication + Logging ----------")

handler = LoggingMiddleware(
    AuthenticationMiddleware(
        Application()
    )
)

print(handler.handle("GET /users token"))