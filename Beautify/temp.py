# def Exercise3(nums1, nums2, nums3, nums4):
#     result = []
#     sum_abc = []

#     for a in range(len(nums1)):
#         for b in range(len(nums2)):
#             for c in range(len(nums3)):
#                 sum_abc.append([[a , b , c] , nums1[a]+nums2[b]+nums3[c]])

#     for i in range(len(sum_abc)):
#         target_value = ((-1)*sum_abc[i][1])
#         if target_value in nums4:
#             index = nums4.index(target_value)
#             sum_abc[i][1] = sum_abc[i][1] + target_value
#             sum_abc[i][0].append(index)
    
#     for i in range(len(sum_abc)):        
#         if len(sum_abc[i][0]) == 4:
#             result.append(tuple(sum_abc[i][0]))

#     return result

# # Example usage
# nums1 = [1, 2, 3, -1]
# nums2 = [-2, -1, 0, 2]
# nums3 = [0, 2, -1, 1]
# nums4 = [-1, 0, 2, -1]
# result = Exercise3(nums1, nums2, nums3, nums4)
# print(result)


