def warehouses_sort(warehouses_list: list) -> tuple:

    np_warehouses_ukr = {}
    np_warehouses_ru = {}

    for warehouse in warehouses_list:
        new_ware_key = warehouse['SettlementRef']
        if new_ware_key in np_warehouses_ukr:
            np_warehouses_ukr[new_ware_key].append(warehouse['Description'])
            np_warehouses_ru[new_ware_key].append(warehouse['DescriptionRu'])
        else:
            np_warehouses_ukr[new_ware_key] = [warehouse['Description']]
            np_warehouses_ru[new_ware_key] = [warehouse['DescriptionRu']]
    
    return (np_warehouses_ukr, np_warehouses_ru)