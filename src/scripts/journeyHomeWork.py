from services.WorkJouneyStatusServices import publish_journey_status


if __name__ == "__main__":
    publish_journey_status("23 rue leon blum Clichy 92110,FR", "40 rue du colisee , Paris, FR")
    print("End of work journey program")