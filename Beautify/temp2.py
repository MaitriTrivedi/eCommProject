def Exercise3(nums1, nums2, nums3, nums4):
    result = []
    sum_ab = {}

    for i, a in enumerate(nums1):
        for j, b in enumerate(nums2):
            if a + b not in sum_ab:
                sum_ab[a + b] = []
            sum_ab[a + b].append((i, j))

    for k, c in enumerate(nums3):
        for l, d in enumerate(nums4):
            target_sum = -1 * (c + d)
            if target_sum in sum_ab:
                for pair in sum_ab[target_sum]:
                    result.append(pair + (k, l))

    return result

# Example usage
nums1 = [1, 2, 3, -1]
nums2 = [-2, -1, 0, 2]
nums3 = [0, 2, -1, 1]
nums4 = [-1, 0, 2, -1]

result = Exercise3(nums1, nums2, nums3, nums4)
print(result)
