def merge_sort(arr):
    """
    Sort an array using the recursive merge sort algorithm.
    
    Args:
        arr (list): List of comparable elements to be sorted.
        
    Returns:
        list: A new sorted list in ascending order.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    """
    Merge two sorted lists into a single sorted list.
    
    Args:
        left (list): First sorted list.
        right (list): Second sorted list.
        
    Returns:
        list: Merged sorted list.
    """
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Drain remaining elements from left
    while i < len(left):
        result.append(left[i])
        i += 1

    # Drain remaining elements from right
    while j < len(right):
        result.append(right[j])
        j += 1

    return result


if __name__ == "__main__":
    sample = [9, 7, 5, 3, 1, 8, 2, 4, 6]
    print(f"Original: {sample}")
    print(f"Sorted:   {merge_sort(sample)}")
