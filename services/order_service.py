
import re

PRODUCTS = {
    "rice": {
        "price": 60,
        "aliases": ["rice", "chawal", "चावल", "బియ్యం"]
    },
    "milk": {
        "price": 30,
        "aliases": ["milk", "doodh", "दूध", "పాలు"]
    },
    "sugar": {
        "price": 45,
        "aliases": ["sugar", "cheeni", "चीनी", "చక్కెర"]
    },
    "bread": {
        "price": 40,
        "aliases": ["bread", "ब्रेड", "రొట్టె"]
    },
    "oil": {
        "price": 150,
        "aliases": ["oil", "तेल", "నూనె"]
    },
    "eggs": {
        "price": 7,
        "aliases": ["eggs", "egg", "अंडे", "గుడ్లు"]
    }
}

NUMBER_WORDS = {
    # English
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,

    # Hinglish
    "ek": 1,
    "do": 2,
    "teen": 3,
    "char": 4,
    "paanch": 5,

    # Hindi
    "एक": 1,
    "दो": 2,
    "तीन": 3,
    "चार": 4,
    "पांच": 5,

    # Telugu
    "ఒకటి": 1,
    "రెండు": 2,
    "మూడు": 3,
    "నాలుగు": 4,
    "ఐదు": 5
}



def extract_order(text):
    text_lower = text.lower()
    order = []

    unit_pattern = (
        r"(?:kg|kgs|kilo|kilos|kilogram|"
        r"litre|liter|liters|l|packet|pack|"
        r"pieces|piece|किलो|किलोग्राम|लीटर|"
        r"కిలోలు|కిలో|లీటర్|లీటర్లు)?"
    )

    for product, details in PRODUCTS.items():

        for alias in details["aliases"]:

            alias_lower = alias.lower()

            pattern = (
                r"(\d+|"
                + "|".join(
                    re.escape(word)
                    for word in NUMBER_WORDS
                )
                + r")\s*"
                + unit_pattern
                + r"\s*"
                + re.escape(alias_lower)
            )

            match = re.search(pattern, text_lower)

            if match:
                quantity_text = match.group(1)

                if quantity_text.isdigit():
                    quantity = int(quantity_text)
                else:
                    quantity = NUMBER_WORDS[quantity_text]

                quantity = max(1, min(quantity, 100))

                order.append({
                    "product": product,
                    "quantity": quantity,
                    "unit_price": details["price"],
                    "total": quantity * details["price"]
                })

                break

            # Product mentioned without quantity
            if alias_lower in text_lower:
                order.append({
                    "product": product,
                    "quantity": 1,
                    "unit_price": details["price"],
                    "total": details["price"]
                })

                break

    return {
        "items": order,
        "total_amount": sum(
            item["total"] for item in order
        ),
        "item_count": len(order)
    }



def create_response(order, language="en"):
    if not order["items"]:
        if language == "hi":
            return "माफ कीजिए, मुझे कोई उत्पाद नहीं मिला। कृपया दोबारा बताएं।"
        if language == "te":
            return "క్షమించండి, ఉత్పత్తులు గుర్తించబడలేదు. దయచేసి మళ్లీ చెప్పండి."
        return "Sorry, I couldn't identify any products. Please try again."

    if language == "hi":
        return (
            f"आपका ऑर्डर तैयार है। "
            f"{order['item_count']} प्रकार के उत्पाद मिले। "
            f"कुल अनुमानित राशि {order['total_amount']} रुपये है। "
            f"कृपया ऑर्डर की पुष्टि करें।"
        )

    if language == "te":
        return (
            f"మీ ఆర్డర్ సిద్ధంగా ఉంది. "
            f"{order['item_count']} రకాల ఉత్పత్తులు గుర్తించబడ్డాయి. "
            f"మొత్తం అంచనా ధర {order['total_amount']} రూపాయలు. "
            f"దయచేసి ఆర్డర్‌ను నిర్ధారించండి."
        )

    return (
        f"Your order is ready. "
        f"{order['item_count']} product types identified. "
        f"Estimated total is {order['total_amount']} rupees. "
        f"Please confirm your order."
    )
