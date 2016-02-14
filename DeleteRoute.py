import Agency

route_id = input("Please provide the Id of the route you want to delete: ")

agency = Agency.Agency.add_gtfs()
agency.delete_line(route_id)
agency.print()
agency.print_to_console()
