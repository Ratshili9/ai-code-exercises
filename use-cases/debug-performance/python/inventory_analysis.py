# inventory_analysis.py
def find_product_combinations(products, target_price, price_margin=10):
    """
    Find all pairs of products where the combined price is within
    the target_price ± price_margin range.

    Args:
        products: List of dictionaries with 'id', 'name', and 'price' keys
        target_price: The ideal combined price
        price_margin: Acceptable deviation from the target price

    Returns:
        List of dictionaries with product pairs and their combined price
    """
    # Optimization: Sort products by price to enable binary search windowing
    # Time complexity reduced from O(N^3) to O(N log N + K)
    import bisect

    results = []
    sorted_products = sorted(products, key=lambda p: p['price'])
    prices = [p['price'] for p in sorted_products]

    min_target = target_price - price_margin
    max_target = target_price + price_margin

    for i, product1 in enumerate(sorted_products):
        p1_price = product1['price']
        
        # Binary search for valid price range for product2
        min_p2 = min_target - p1_price
        max_p2 = max_target - p1_price

        # Search only for j > i to avoid self-pairing and duplicates
        left_idx = max(i + 1, bisect.bisect_left(prices, min_p2))
        right_idx = bisect.bisect_right(prices, max_p2)

        for j in range(left_idx, right_idx):
            product2 = sorted_products[j]
            combined_price = p1_price + product2['price']
            pair = {
                'product1': product1,
                'product2': product2,
                'combined_price': combined_price,
                'price_difference': abs(target_price - combined_price)
            }
            results.append(pair)

    # Sort by price difference from target
    results.sort(key=lambda x: x['price_difference'])
    return results

# Example usage
if __name__ == "__main__":
    import time
    import random

    # Generate a large list of products
    print("Generating Product List")
    product_list = []
    for i in range(5000):
        product_list.append({
            'id': i,
            'name': f'Product {i}',
            'price': random.randint(5, 500)
        })

    # Measure execution time
    print(f"Finding product combinations for {len(product_list)} products")
    start_time = time.time()
    combinations = find_product_combinations(product_list, 500, 50)
    end_time = time.time()

    print(f"Found {len(combinations)} product combinations")
    print(f"Execution time: {end_time - start_time:.2f} seconds")