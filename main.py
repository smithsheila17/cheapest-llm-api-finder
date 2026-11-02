from __future__ import annotations
import json
from dataclasses import dataclass

@dataclass(frozen=True)
class Offer:
    model: str
    provider: str
    input_price: float  # USD per 1M tokens
    output_price: float

OFFERS = [
    Offer("gpt-4o-mini", "provider-a", 0.15, 0.60),
    Offer("gpt-4o-mini", "provider-b", 0.12, 0.55),
    Offer("llama-3.1-70b", "provider-c", 0.20, 0.80),
    Offer("llama-3.1-70b", "provider-d", 0.18, 0.90),
]

def estimate_cost(offer, input_tokens, output_tokens):
    return (input_tokens / 1_000_000 * offer.input_price +
            output_tokens / 1_000_000 * offer.output_price)

def find_cheapest(model, input_tokens=1000, output_tokens=500):
    candidates = [o for o in OFFERS if o.model == model]
    if not candidates:
        raise ValueError(f"No offers for model: {model}")
    ranked = sorted(candidates, key=lambda o: estimate_cost(o, input_tokens, output_tokens))
    best = ranked[0]
    return {
        "model": model,
        "provider": best.provider,
        "estimated_cost_usd": round(estimate_cost(best, input_tokens, output_tokens), 6),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }

def list_models():
    return sorted({o.model for o in OFFERS})

if __name__ == "__main__":
    print("Available models:", ", ".join(list_models()))
    print(json.dumps(find_cheapest("gpt-4o-mini", 1000, 500), indent=2))
