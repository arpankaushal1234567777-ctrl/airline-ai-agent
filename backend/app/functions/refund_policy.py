REFUND_RULES = {
    "fully refundable": {
        "refund_type": "Full Refund",
        "base_fare_refundable": True,
        "cancellation_fee_percent": 0,
        "taxes_refundable": True,
        "notes": "Full refund of base fare and taxes. No cancellation penalty.",
    },
    "semi refundable": {
        "refund_type": "Partial Refund",
        "base_fare_refundable": True,
        "cancellation_fee_percent": 25,
        "taxes_refundable": True,
        "notes": "Base fare refunded minus 25% cancellation fee. Taxes fully refundable.",
    },
    "non refundable": {
        "refund_type": "Non-Refundable",
        "base_fare_refundable": False,
        "cancellation_fee_percent": 100,
        "taxes_refundable": True,
        "notes": "Base fare is non-refundable. Only unused taxes and airport charges may be refunded.",
    },
}


def get_refund_policy(fare_type: str):

    fare_type = fare_type.lower().strip()

    if fare_type not in REFUND_RULES:
        return {
            "success": False,
            "message": (
                f"Unknown fare type: '{fare_type}'. "
                "Valid options are: Fully Refundable, Semi Refundable, Non Refundable."
            ),
        }

    policy = REFUND_RULES[fare_type]

    return {
        "success": True,
        "fare_type": fare_type.title(),
        **policy,
    }
