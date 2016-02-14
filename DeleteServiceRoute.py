import Agency

route_id = input("What is the Id of the route? ")
service_id = input("What is the name of the service? ")

agency = Agency.Agency.add_gtfs()
agency.delete_service_of_line(route_id, service_id)
agency.print()
agency.print_to_console()