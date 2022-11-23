# Kindly note that the observations are made for the older version of Program-2 (As discusses with sir, this would be considered for evaluation)

**Observation:** On changing the line while keeping the blocks and ways unchanged, the rate doesn't change in both the programs (1, 2)		
**Reason:** This is because there is no temporal locality.

**Observation:** Number of ways also doesn't affect the hit rate in both the programs (1, 2)
**Reason:** This is becayse there is no temporal locality. The misses aren't because of conflict.

**Observation:** Increasing the number of blocks increases the hit rate in both the programs in both the programs (1, 2)		
**Reason:** This is because of high spatial locality.

**Observation:** For program-1, the write policy with allocate worked significantly better.		
**Reason:** This is because of high spatial locality.

**Observation:** For program-2, the write policy didn't affect the hit rate.		
**Reason:** This is because of poor write spatial locality and errors in program-2.

**Observation:** The hit rate increases (in program-1) slightly when we increase L1 from 8,8 to 16, 16.		
**Reason:** This slightly increase can be ignored, as each of the miss comes from the first access to block in the line, To populate each line we have 3 hits, 1 miss, but for last line we have 1 miss and 1 hit and total number of access are of the form 4x+2. As we increase x the hit rate approaches 75%

**Observation:** This hit rate decreases (in program-2) when we increase L1 from 8,8 to 16, 16. 		
**Reason:** This is because the spatial locality decreases further.

**Observation:** Different presets produce the same result for program-1 and 2 because the blocks aren't being changed.		
**Reason:** The hits are a result of spatial locality, so the number of hits doesn't change.

**Observation:** The hit rate changes for different presets in program-3		
**Reason:** This is because of temporal locality.

