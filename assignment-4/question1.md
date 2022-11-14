The output of the command `getconf -a | grep CACHE` is		
```
LEVEL1_ICACHE_SIZE                 32768
LEVEL1_ICACHE_ASSOC                
LEVEL1_ICACHE_LINESIZE             64
LEVEL1_DCACHE_SIZE                 32768
LEVEL1_DCACHE_ASSOC                8
LEVEL1_DCACHE_LINESIZE             64
LEVEL2_CACHE_SIZE                  524288
LEVEL2_CACHE_ASSOC                 8
LEVEL2_CACHE_LINESIZE              64
LEVEL3_CACHE_SIZE                  8388608
LEVEL3_CACHE_ASSOC                 0
LEVEL3_CACHE_LINESIZE              64
LEVEL4_CACHE_SIZE                  
LEVEL4_CACHE_ASSOC                 
LEVEL4_CACHE_LINESIZE              
```

1. There are three levels of cache
2. Cache size are given in the table below

|Level|Size|
|-----------|-----------|
|1|32768(instruction cache) + 32768(data cache)=65536 bytes = 64 KiB|
|2|524288 bytes = 512 KiB |
|3|8388608 bytes = 8 MiB|
	
3. Associativity of Level-1 cache (Instruction) = 0		
Associativity of Level-1 cache (data) = 8		
Associativity of Level-2 cache = 8		
Associativity of Level-3 cache = 0		

4. My CPU has 6 cores. Since L1 and L2 have 6 instances, one for each core we would have		
6 * (64 KiB) + 6 * (512 KiB) + 8 MiB = 8 MiB + 3 MiB + 384 KiB = 11.384 MiB

