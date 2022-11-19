- First, we observe that on changing the lines while keeping the blocks and ways as constant, the hit rate doesn't change. This is because as we observe that program reads the data at that address only once, there is no temporal locality observed in these programs.

- Number of ways also doesn't affect the hit rate(in program 1 and program 2) for the same reason as above, since we aren't reading the value in that address again.

- Increasing number of blocks increases the hit rate because of the spatial locality. 

- For program-1 write policy with allocate worked significantly better, this is because in program-1 we are acessing the data present in consecutive bytes, this increases the spatial locality. Even if the block size is small, it still reads values which are already present in the cache.

- For program-2 write policy didn't affect the hit rate, this is because of poor spatial locality.

- The hit rate increases (in program-1) slightly when we increase L1 from 8,8 to 16, 16. This effect can be ignored.

- This hit rate decreases (in program-2) when we increase L1 from 8,8 to 16, 16. This is because the spatial locality decreases further.
