from src.services.DeleteAppService import DeleteAppService

def delete_apps():
    """
    Initializes the DeleteAppService and calls the method to delete all custom apps.
    """
    delete_service = DeleteAppService()
    print("Attempting to delete all custom transport and financial apps...")
    delete_service.delete_all_apps()
    print("Deletion requests sent.")

if __name__ == "__main__":
    delete_apps()
