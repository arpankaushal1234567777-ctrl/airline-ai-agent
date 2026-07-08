ALLOWANCE = {
    "economy": 23,
    "premium economy": 35,
    "business": 40,
    "first": 50,
}

EXTRA_FEE_PER_KG = 1000


def calculate_baggage_fee(travel_class: str, baggage_weight: float):

    travel_class = travel_class.lower().strip()

    if travel_class not in ALLOWANCE:
        return {
            "success": False,
            "message": "Invalid travel class."
        }

    allowed_weight = ALLOWANCE[travel_class]

    extra_weight = max(0, baggage_weight - allowed_weight)

    fee = extra_weight * EXTRA_FEE_PER_KG

    return {
        "success": True,
        "travel_class": travel_class.title(),
        "allowed_weight": allowed_weight,
        "baggage_weight": baggage_weight,
        "extra_weight": extra_weight,
        "fee": fee,
    }