import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "Guest")
    return func.HttpResponse(f"Hello {name}! Your GitHub-integrated Azure Function works 🎉")
