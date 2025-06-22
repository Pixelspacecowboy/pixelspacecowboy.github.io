import time  # For performance benchmarking
from bisect import bisect_left  # Efficient binary search support
from collections import defaultdict  # Hash map structure for grouping

# Merge Sort implementation for sorting list of tuples by score
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# New algorithm: Quick Sort implementation
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    less = [x for x in arr[1:] if x[1] <= pivot[1]]
    greater = [x for x in arr[1:] if x[1] > pivot[1]]
    return quick_sort(less) + [pivot] + quick_sort(greater)

# Binary Search using bisect for sorted list of tuples
def binary_search(data, target):
    idx = bisect_left([x[1] for x in data], target)
    if idx < len(data) and data[idx][1] == target:
        return data[idx]
    return None  # Not found

# New data structure: Hash map to group students by score
def group_students_by_score(students):
    grouped = defaultdict(list)
    for name, score in students:
        grouped[score].append(name)
    return grouped

# Utility function to print list of student-score pairs
def view_students(data):
    for name, score in data:
        print(f"{name}: {score}")

# Main execution
if __name__ == "__main__":
    # Sample student data
    students = [
        ("Alice", 91),
        ("Bob", 88),
        ("Charlie", 93),
        ("Diana", 85),
        ("Evan", 88)
    ]

    print("Original Data:")
    view_students(students)

    # Benchmark merge sort
    start = time.perf_counter()
    sorted_students_merge = merge_sort(students)
    end = time.perf_counter()
    print("\nSorted (Merge Sort):")
    view_students(sorted_students_merge)
    print(f"Merge Sort Time: {end - start:.6f} seconds")

    # Benchmark quick sort
    start = time.perf_counter()
    sorted_students_quick = quick_sort(students)
    end = time.perf_counter()
    print("\nSorted (Quick Sort):")
    view_students(sorted_students_quick)
    print(f"Quick Sort Time: {end - start:.6f} seconds")

    # Binary search for score 88
    target_score = 88
    start = time.perf_counter()
    result = binary_search(sorted_students_merge, target_score)
    end = time.perf_counter()
    print(f"\nBinary Search for score {target_score}: {result}")
    print(f"Search Time: {end - start:.6f} seconds")

    # Grouping using a hash map
    score_groups = group_students_by_score(students)
    print(f"\nStudents who scored {target_score}: {score_groups[target_score]}")

